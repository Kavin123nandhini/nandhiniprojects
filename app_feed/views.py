from django.shortcuts import render, redirect, get_object_or_404

# Create your views here.
# views.py
from django.db import models
from app_restapi.models import UserRegistration
from django.contrib.auth.models import User
from django.db.models import Q
from django.http import JsonResponse
from django.contrib import messages
from app_authuser import views
from django.template.loader import render_to_string
from PostMan import common
from .models import Friends, Messages, JobAppliedUser

from .models import JobListing


def search_friends(request):
    if common.is_authendicated(request):
        print("search start")
        if request.method == 'GET':
            query = request.GET.get('formData')
            results = []

            print("query:", query)
            # Get the 'q' parameter from the URL, default to an empty string if
            # not provided

            if query:
                # Create a complex query using Q objects to search in both models
                results = UserRegistration.objects.filter(
                    Q(user__first_name__icontains=query) |  # Search usernames in the User model
                    Q(user__email__icontains=query) |  # Search emails in the User model
                    Q(phonenumber__icontains=query)
                    # Search specific field in the UserProfile model (customize this)
                ).distinct()
                print("search results", results)
                results_data = [
                    {'name': user.user.first_name, 'email': user.user.email,
                     'id': user.user.id, 'phonenumber': user.phonenumber}
                    for user in results]
                # If it's an AJAX request, return JSON response with search results
                data = {'results': results_data}
                return JsonResponse(data)
            else:
                return redirect('my-network')
        return redirect('my-network')
    messages.error(request, "please login again")
    return redirect('home')


def add_friend(request):
    if common.is_authendicated(request):
        current_user = common.get_user(request.session['user_email'])
        print("user_id:", current_user.id)
        add_id = request.GET.get('id')
        print("add_id:", id)
        friend = User.objects.get(id=add_id)
        try:
            # Check if a friendship already exists
            existing_friendship = Friends.objects.get(user=current_user,
                                                      friend_id=add_id)
        except Friends.DoesNotExist:
            # If no existing friendship, create a new one
            new_friendship = Friends(user=current_user, friend_id=add_id)
            new_friendship.save()

            # Redirect to a page displaying the user's friends or a confirmation
            # message
        return redirect('my-network')
    messages.error(request, "please login again")
    return redirect('home')


#
#
# def view_friends(request):
#     # Get the currently logged-in user
#     current_user = common.get_user(request.session['user_email'])
#
#     # Retrieve the user's friends (assuming 'accepted' is the status of
#     # accepted friendships)
#     friends = Friends.objects.filter(user=current_user, status='accepted')
#     print("friends",friends)
#
#     # Render a template and pass the 'friends' queryset to it
#     return render(request, 'my-network.html', {'friends': friends})


# views.py

# def view_friend_requests(request):
#     # Get the currently logged-in user
#     current_user = common.get_user(request.session['user_email'])
#
#     # Retrieve pending friend requests (assuming 'pending' is the status for
#     # pending requests)
#     friend_requests = Friends.objects.filter(friend=current_user,
#                                              status='pending')
#
#     # Render a template and pass the 'friend_requests' queryset to it
#     return render(request, 'my-network.html',
#                   {'friend_requests': friend_requests})


def accept_friend_request(request, request_id):
    if common.is_authendicated(request):
        current_user = common.get_user(request.session['user_email'])
        friend_request = get_object_or_404(Friends, id=request_id)

        # Mark the request as accepted (update the 'status' field)
        friend_request.status = 'accepted'
        friend_request.save()
        friends = Friends.objects.create(user=current_user,
                                         friend_id=request_id
                                         , status="accepted")

        return redirect('my-network')
    messages.error(request, "please login again")
    return redirect('home')


def reject_friend_request(request, request_id):
    friend_request = get_object_or_404(Friends, id=request_id)

    # Mark the request as rejected (update the 'status' field)
    friend_request.status = 'rejected'
    friend_request.save()

    return redirect('my-network')


def send_message(request):
    current_user = common.get_user(request.session['user_email'])
    print("send message")
    contex = {}
    if request.method == 'POST':
        post = request.POST.get("user-post")

        is_public = request.POST.get(
            'is_public') == 'on'  # if checked means return on
        print(post, is_public)
        sender1 = current_user
        if is_public:
            all_users = User.objects.all()
            for user in all_users:
                message = Messages(sender=sender1, receiver=user,
                                   content=post)
                message.save()

        else:
            # friends = Friends.objects.filter(user_id=sender)
            # print(friends)
            friends = Friends.objects.filter(user=current_user,
                                             status='accepted')
            print(friends)
            # Create and save a message for each friend
            if friends.exists():
                for friend in friends:
                    message = Messages(sender=sender1, receiver=friend.friend,
                                       content=post)
                    message.save()
            else:
                messages.error(request,
                               'Currently Your have any friends.Please add friends!')

    return redirect('feed')


def post_job(request):
    if common.is_authendicated(request):
        current_user = common.get_user(request.session['user_email'])
        if request.method == 'POST':
            title = request.POST.get('title')
            description = request.POST.get('description')
            posted_by = current_user

            # Create a new job listing
            job_listing = JobListing(title=title, description=description,
                                     posted_by=posted_by)
            job_listing.save()

            # Redirect to a page displaying job listings or a confirmation page
            return redirect('post-job')
            # Replace 'job_listings' with your actual job listings page URL
        posted_jobs = JobListing.objects.filter(posted_by=current_user)
        if not posted_jobs:
            return render(request, "post-job.html")
        return render(request, "post-job.html", {'job_listing': posted_jobs})
    messages.error(request, "please login again")
    return redirect('home')


def view_job(request, id):
    if common.is_authendicated(request):
        current_user = common.get_user(request.session['user_email'])
        remarks=None
        job = get_object_or_404(JobListing, id=id)
        try:
            applied = JobAppliedUser.objects.get(job=job,applied_user=current_user)
            print(applied.job)
            if applied:
                remarks=applied.remarks
            return render(request, 'view-job-decs.html',
                          {'job': job,'remarks':remarks})
        except JobAppliedUser.DoesNotExist:
            return render(request, 'view-job-decs.html',
                          {'job': job, 'remarks': remarks})

    messages.error(request, "please login again")
    return redirect('home')


def apply_job(request, id):
    # view and apply for the job
    context = {}
    if common.is_authendicated(request):
        current_user = common.get_user(request.session['user_email'])

        job = get_object_or_404(JobListing, id=id)
        applied = False

        if job:

            job_apply = JobAppliedUser.objects.create(job=job,
                                                      applied_user=current_user)
            job_apply.save()


        context = {
            'job': job,
            }
        messages.success(request, "Job applied Sucessfully!,")
        return redirect("view-job",id)

        # viewing applied jobs
    messages.error(request, "please login again")
    return redirect('home')


def view_applied_list(request):
    if common.is_authendicated(request):
        current_user = common.get_user(request.session['user_email'])
        my_job_listings = JobListing.objects.filter(posted_by=current_user)
        # applied_users = JobAppliedUser.objects.filter(job__in=my_job_listings)
        # Retrieve applied users for those job listings
        applied_users = JobAppliedUser.objects.filter(Q(job__in = my_job_listings) & Q(remarks='hold'))

        return render(request, 'view-applied-list.html',
                      {'applied_users': applied_users})

    messages.error(request, "please login again")
    return redirect('home')


def accept_result(request, id):
    applied_users = JobAppliedUser.objects.get(id=id)
    applied_users.remarks = 'accept'
    applied_users.save()
    return redirect('view-applied-list')


def ignore_result(request, id):
    applied_users = JobAppliedUser.objects.get(id=id)
    applied_users.remarks = 'ignore'
    applied_users.save()
    return redirect('view-applied-list')


def hold_result(request, id):
    applied_users = JobAppliedUser.objects.get(id=id)
    applied_users.remarks = 'hold'
    applied_users.save()
    return redirect('view-applied-list')
