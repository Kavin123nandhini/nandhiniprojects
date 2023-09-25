from datetime import datetime, timezone, timedelta

import requests as req1
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from app_restapi.models import UserRegistration
from app_feed.models import Friends, Messages, JobListing
from django.contrib.auth.models import User
# Verification email
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage


# Create your views here.
def home(request):
    if request.user.is_authenticated:
        request.session['username'] = request.user.first_name
        return render(request,"home.html",{'user': request.user})
    return render(request, "home.html",)


# user registration page request
def register_link(request):
    return render(request, "signup.html")


def user_role(request):
    if request.method == 'POST':
        role = request.POST.get('user_role')
    return render(request, "signup.html", {'user_role': role})


# getting user registration details request
def user_register(request):
    context = {}
    print("user register")
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
        about_company = request.POST.get("about_company")
        industry_type = request.POST.get("industry_type")
        print("emirates_id", emirates_id)
        if UserRegistration.objects.filter(emirates_id=emirates_id).exists():
            messages.error(request,
                           'Your emirates_id already exists!')
            return redirect('home')

        user_data = {
            "first_name": first_name,
            "last_name": last_name,
            "username": email,
            "email": email,
            "password": password,
        }
        try:
            user_instance = User.objects.create_user(**user_data)
            context = {
                "phonenumber": phonenumber,
                "user": user_instance,
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
                "about_company": about_company,
                "industry_type": industry_type,
            }

            # or user conflict status code 409
            # passing user nested dict details and getting response
            try:
                reg_instance = UserRegistration.objects.create(**context)
                messages.success(request,
                                 'Registered successfully!Please login '
                                 'PostMan!')
                return redirect('home')

            except Exception as e:
                print(f"An error occurred for user registration: {e}")
        except Exception as e:
            print(f"user table not found: {e}")

    return redirect("register-link")


def user_login(request):
    if request.method == 'POST':
        username = request.POST.get("username")
        password = request.POST.get("password")
        print(username,password)
        user = authenticate(username=username, password=password)
        print(user)
        if user:
            # Check it the account is active
            if user.is_active:
                login(request, user)
                return redirect('feed')
            else:
                messages.error(request, 'username or password incorrect !')
        else:
            messages.error(request, 'User not found !')
    return render(request, "home.html")


@login_required
def user_logout(request):
    try:
        logout(request)
        messages.info(request, 'You are logging out!')
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
        # request.session['uid'] = uid
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
            id = request.user
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
    if request.user.is_authenticated:
        current_user = request.user
        post_message = Messages.objects.filter(receiver=current_user)
        job_listing = JobListing.objects.all()
        print("messages", post_message)
        return render(request, 'after-login-page.html',
                      {'post_message': post_message,
                       'job_listing': job_listing,'user': request.user})
    messages.error(request, "please login again")
    return redirect('home')


def my_network(request):
    if request.user.is_authenticated:
        current_user = request.user
        context = {}
        # Retrieve pending friend requests (assuming 'pending' is the status for
        # pending requests)
        friend_requests = Friends.objects.filter(friend=current_user,
                                                 status='pending')
        friends = Friends.objects.filter(user=current_user, status='accepted')

        print("friends", friends)
        contex = {
            'friend_requests': friend_requests,
            'friends': friends,
        }
        # Render a template and pass the 'friend_requests' queryset to it
        return render(request, 'my-network.html', contex)
    messages.error(request, "please login again")
    return redirect("home")
