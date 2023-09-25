from django.contrib.auth.models import User
from django.db import models
from django.core.validators import RegexValidator
import uuid

numeric = RegexValidator(r'^[0-9+]', 'Only digit characters.')


class UserRegistration(models.Model):
    user_reg_id = models.UUIDField(primary_key=True, editable=False,
                                   unique=True,
                                   default=uuid.uuid4)
    emirates_id = models.CharField(max_length=200,
                                   unique=True)
    user = models.OneToOneField(User, related_name='user'
                             , on_delete=models.CASCADE)
    user_role = models.CharField(null=True, max_length=30)
    emirates_office = models.CharField(null=True, max_length=30)
    phonenumber = models.CharField(max_length=30)
    gender=models.CharField(max_length=30,null=True,blank=True)
    qualification = models.CharField(max_length=30, null=True, blank=True)
    university = models.CharField(max_length=30, blank=True, null=True)
    year_passed_out = models.CharField(max_length=30, blank=True, null=True)
    skills = models.CharField(max_length=500, blank=True, null=True)
    exp_years = models.CharField(max_length=30, blank=True, null=True)
    designation = models.CharField(max_length=30, blank=True, null=True)
    work_company = models.CharField(max_length=30, blank=True, null=True)
    about_company = models.TextField(max_length=1000, null=True, blank=True)
    employee_count = models.CharField(max_length=30, blank=True,
                                       null=True)
    industry_type=models.CharField(max_length=100, null=True, blank=True)
    auth_name = models.CharField(max_length=30, blank=True,
                                 null=True)
    date_of_registration = models.DateTimeField(auto_now_add=True, null=True,
                                                db_index=True)


