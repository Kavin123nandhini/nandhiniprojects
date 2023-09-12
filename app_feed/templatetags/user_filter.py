from django.shortcuts import get_object_or_404

from app_restapi.models import UserRegistration, User
from PostMan import common
from app_feed.models import JobListing, JobAppliedUser

from django import template

register = template.Library()


# template tags for getting course material for based on course id


@register.filter(is_safe=True)
def user_profile(user):
    try:
        obj = UserRegistration.objects.get(user=user)
    except UserRegistration.DoesNotExist:
        obj = None
    return obj


@register.filter
def user_company(user):
    try:
        obj = UserRegistration.objects.get(user=user)
    except UserRegistration.DoesNotExist:
        obj = None
    return obj.work_company


@register.filter
def user_remark(obj, user):
    try:
        obj = JobAppliedUser.objects.get(user=user)
    except JobAppliedUser.DoesNotExist:
        obj = None
    return obj.remarks

# @register.filter
# def check_approval(user_id, course_id):
#     obj = get_object_or_404(CourseEnroll, user_id=user_id,
#                             course_id=course_id)
#     print("obj.is_approved", obj.is_approved)
#     if not obj.is_approved:
#         return True
#     return False
