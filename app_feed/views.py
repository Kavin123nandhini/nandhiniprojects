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


def jobs_page(request):
    current_user = request.user
    applied_jobs = JobAppliedUser.objects.filter(applied_user=current_user)
    user = UserRegistration.objects.get(user_id=current_user.id)
    query = 'python,sql'

    skills_set= query.split(',')

    filter_query = Q()

    # Iterate through skills_set and create Q objects for each skill
    for skill in skills_set:
        filter_query |= Q(skills_req__icontains=skill)
    matching_skills = JobListing.objects.filter(filter_query)
    context = {
        'job_listing': matching_skills,
        'applied_jobs': applied_jobs,
    }

    # if not matching_skills:  # Check if there are no matching skills
    #     context['no_matching_jobs'] = True  # Add a flag to the context
    return render(request, 'jobs-page.html', context)


def search_friends(request):
    if request.user.is_authenticated:
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
    if request.user.is_authenticated:
        current_user = request.user
        print("user_id:", current_user.id)
        add_id = request.GET.get('id')
        print("add_id:", add_id)
        friend = User.objects.get(id=add_id)
        print("Friend:", friend)
        friend_request_exists = Friends.objects.filter(
            friend_id=current_user.id, user_id=friend.id,
            status="pending").exists()
        print("friend_request_exists", friend_request_exists)
        if friend_request_exists:
            messages.info(request, "Please accept user invitation")
            return redirect('my-network')
        try:
            # Check if a friendship already exists
            existing_friendship = Friends.objects.get(user=current_user,
                                                      friend=friend)
            print("checking current user")

            if existing_friendship.status == "pending":
                messages.error(request, "Already request send")
            elif existing_friendship.status == "accepted":
                messages.error(request, "Already in your contact")
            else:
                print("user")

        except Friends.DoesNotExist:
            # If no existing friendship, create a new one
            new_friendship = Friends(user=current_user, friend=friend)
            new_friendship.save()
            if friend == current_user:
                new_friendship.status = "accepted"
                new_friendship.save()
                messages.info(request, "Added")
                return redirect('my-network')
            # Redirect to a page displaying the user's friends or a confirmation
            # message
            messages.success(request, "Friend request send")
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
    if request.user.is_authenticated:
        current_user = request.user
        friend_request = get_object_or_404(Friends, id=request_id)

        # Mark the request as accepted (update the 'status' field)
        friend_request.status = 'accepted'
        friend_request.save()
        Friends.objects.create(user_id=friend_request.friend_id,
                               friend_id=current_user.id,
                               status="accepted")
        messages.info(request, "Request accepted")

        return redirect('my-network')
    messages.error(request, "Please login again")
    return redirect('home')


def reject_friend_request(request, request_id):
    friend_request = get_object_or_404(Friends, id=request_id)

    # Mark the request as rejected (update the 'status' field)
    friend_request.status = 'rejected'
    friend_request.save()

    return redirect('my-network')


def send_message(request):
    current_user = request.user
    if request.method == 'POST':
        post = request.POST.get("user-post")

        is_public = request.POST.get(
            'is_public') == 'on'  # if checked means return on
        sender1 = current_user
        if is_public:
            all_users = User.objects.all()
            for user in all_users:
                message = Messages(sender=sender1, receiver=user,
                                   content=post)
                message.save()

        else:
            friends = Friends.objects.filter(user=current_user,
                                             status='accepted')
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
    if request.user.is_authenticated:
        current_user = request.user
        if request.method == 'POST':
            title = request.POST.get('title')
            description = request.POST.get('description')
            job_type = request.POST.get('job_type')
            skills_req = request.POST.get('skills_req')
            posted_by = current_user

            # Create a new job listing
            job_listing = JobListing(title=title, description=description,
                                     posted_by=posted_by,
                                     skills_req=skills_req, job_type=job_type)
            job_listing.save()

            # Redirect to a page displaying job listings or a confirmation page
            return redirect('post-job')
            # Replace 'job_listings' with your actual job listings page URL
        posted_jobs = JobListing.objects.filter(posted_by=current_user)
        if not posted_jobs:
            messages.info(request, "You are not posting any jobs")
            return redirect("feed")
        return render(request, "post-job.html", {'job_listing': posted_jobs})
    messages.error(request, "please login again")
    return redirect('home')


def view_job(request, id):
    if request.user.is_authenticated:
        current_user = request.user
        remarks = None
        jobs = get_object_or_404(JobListing, id=id)
        try:
            applied = JobAppliedUser.objects.get(job=jobs,
                                                 applied_user=current_user)
            if applied:
                remarks = applied.remarks
            return render(request, 'view-job-decs.html',
                          {'jobs': jobs, 'remarks': remarks})
        except JobAppliedUser.DoesNotExist:
            return render(request, 'view-job-decs.html',
                          {'jobs': jobs, 'remarks': remarks})

    messages.error(request, "please login again")
    return redirect('home')


def apply_job(request, id):
    # view and apply for the job
    context = {}
    if request.user.is_authenticated:
        current_user = request.user

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
        return redirect("view-job", id)

        # viewing applied jobs
    messages.error(request, "please login again")
    return redirect('home')


def view_applied_list(request):
    if request.user.is_authenticated:
        current_user = request.user
        my_job_listings = JobListing.objects.filter(posted_by=current_user)
        # applied_users = JobAppliedUser.objects.filter(job__in=my_job_listings)
        # Retrieve applied users for those job listings
        applied_users = JobAppliedUser.objects.filter(
            Q(job__in=my_job_listings) & Q(remarks='pending'))
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


def cancel_applied(request,id):
    applied_users = JobAppliedUser.objects.get(id=id)
    if applied_users:
        applied_users.delete()
        messages.info(request,"Application successfully canceled")
    return redirect('jobs-page')


