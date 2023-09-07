from datetime import datetime, timezone, timedelta

import requests as req1
from django.contrib import messages
from django.shortcuts import render, redirect
from django.core.exceptions import ObjectDoesNotExist
from django.urls import reverse
from app_restapi.models import UserRegistration, User
from app_feed.models import Friends, Messages, JobListing
from PostMan import common
from django.db.models import Q
# from .forms import ContactForm
# Verification email
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage


# Create your views here.
def home(request):
    if common.is_authendicated(request):
        user = common.get_user(request.session['user_email'])
        print("user_id:", user.id)
        request.session['username'] = user.first_name
    return render(request, "home.html")


# user registration page request
def register_link(request):
    return render(request, "signup.html")


def user_role(request):
    if request.method == 'POST':
        role = request.POST.get('user_role')
    print(role)
    return render(request, "signup.html", {'user_role': role})


# getting user registration details request
def user_register(request):
    context = {}
    print("user register")
    # assign registration api url to var url
    url = common.register_api_url
    if request.method == 'POST':
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        emirates_id = request.POST.get("emirates_id")
        email = request.POST.get("email")
        password = request.POST.get("password")
        phonenumber = request.POST.get("phone")
        gender = request.POST.get("gender")
        emirates_name = request.POST.get("emirates_name")
        qualification = request.POST.get("qualification")
        university = request.POST.get("university")
        role = request.POST.get("user_role")
        work_exp_years = request.POST.get("work_exp_years")
        designation = request.POST.get("designation")
        work_company = request.POST.get("work_company")
        passed_year = request.POST.get("passed_year")
        skills = request.POST.get("skills")
        employee_count = request.POST.get("employee_count")
        auth_name = request.POST.get("auth_name")
        about_company=request.POST.get("about_company")
        print("emirates_id", emirates_id)
        user = {
            "first_name": first_name,
            "last_name": last_name,
            "username": email,
            "email": email,
            "password": password,
        }
        context = {
            "phonenumber": phonenumber,
            "user": user,
            "emirates_id": emirates_id,
            "gender": gender,
            "qualification": qualification,
            "emirates_office": emirates_name,
            "user_role": role,
            "exp_years": work_exp_years,
            "designation": designation,
            "work_company": work_company,
            "university": university,
            "year_passed_out": passed_year,
            "skills": skills,
            "employee_count": employee_count,
            "auth_name": auth_name,
            "about_company":about_company,
        }
        if User.objects.filter(email=email).exists():
            messages.error(request,
                           'Your e-mail address already exists!')
            return redirect('home')
        if UserRegistration.objects.filter(emirates_id=emirates_id).exists():
            messages.error(request,
                           'Your emirates_id already exists!')
            return redirect('home')

        # or user conflict status code 409
        # passing user nested dict details and getting response
        try:
            res1 = req1.post(url, json=context)
            print(res1.content)
            print(res1, url, context)
            if res1.status_code in range(200, 299):
                messages.success(request,
                                 'Registered successfully!Please login '
                                 'PostMan!')
                return redirect('home')

            else:
                messages.error(request,
                               'Api response failed!')
                return redirect('home')
        except req1.exceptions.RequestException as e:
            raise SystemExit(e)

    return redirect("register_link")


def user_login(request):
    context = {}
    url = common.login_api_url
    if request.method == 'POST':
        username = request.POST.get("username")
        password = request.POST.get("password")
        print(username, password)
        context = {
            "username": username,
            "password": password
        }
        print(context)
        try:
            res1 = req1.post(url, context)
            print(res1)
            if res1.json().get("access", ""):
                access_token = res1.json()["access"];
                refresh_token = res1.json()["refresh"]
                try:
                    request.session['user_email'] = username
                    request.session['access_token'] = access_token
                    request.session['refresh_token'] = refresh_token
                    request.session['logged_in'] = True
                    # messages.success(request, 'Login Successfully!')
                    # print(request.user.email)

                    return redirect('feed')
                except KeyError:
                    messages.error(request,
                                   'Your session time out please login '
                                   'again!')
                    return redirect('home')
            else:
                messages.error(request, 'username or password incorrect !')
            return redirect('home')
        except req1.exceptions.RequestException as e:
            messages.error(request, 'User not found !')
            raise SystemExit(e)
    return render(request, "home.html")


def user_logout(request):
    try:
        print("logging out")
        messages.info(request, 'You are logging out!')
        request.session.flush()
    except KeyError:
        pass
    return redirect('home')


def forgot_password(request):
    if request.method == 'POST':
        email = request.POST['email']
        if User.objects.filter(email=email).exists():
            user = User.objects.get(email__exact=email)
            # Reset password email
            current_site = get_current_site(request)
            mail_subject = 'Reset Your Password'

            message = render_to_string('reset-password-email.html', {
                'user': user,
                'domain': current_site,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user),
            })
            to_email = email
            send_email = EmailMessage(mail_subject, message, to=[to_email])
            send_email.send()

            messages.success(request,
                             'Password reset email has been sent to your '
                             'email address.')
            return redirect('home')
        else:
            messages.error(request, 'Account does not exist!')
            print("no account")
            return redirect('forgot-password')
    return render(request, 'home.html')


def resetpassword_validate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User._default_manager.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        request.session['uid'] = uid
        messages.success(request, 'Please reset your password')
        return redirect('reset-password')
    else:
        messages.error(request, 'This link has been expired!')
        return redirect('home')


def reset_password(request):
    if request.method == 'POST':
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if password == confirm_password:
            uid = request.session.get('uid')
            user = User.objects.get(pk=uid)
            user.set_password(password)
            user.save()
            messages.success(request, 'Password reset successful')
            return redirect('home')
        else:
            messages.error(request, 'Password do not match!')
            return redirect('reset-password')
    else:
        return render(request, 'reset-password.html')


def after_login_page(request):
    if common.is_authendicated(request):
        current_user = common.get_user(request.session['user_email'])
        post_message = Messages.objects.filter(receiver=current_user)
        job_listing = JobListing.objects.all()
        print("messages",post_message)
        return render(request, 'after-login-page.html',{'post_message':post_message,'job_listing':job_listing})
    messages.error(request,"please login again")
    return redirect('home')


def my_network(request):
    if common.is_authendicated(request):
        current_user = common.get_user(request.session['user_email'])
        context={}
        # Retrieve pending friend requests (assuming 'pending' is the status for
        # pending requests)
        friend_requests = Friends.objects.filter(friend=current_user,
                                                 status='pending')
        friends = Friends.objects.filter(user=current_user, status='accepted')

        print("friends", friends)
        contex = {
            'friend_requests': friend_requests,
            'friends' : friends,
        }
        # Render a template and pass the 'friend_requests' queryset to it
        return render(request, 'my-network.html',contex)
    messages.error(request,"please login again")
    return redirect("home")


