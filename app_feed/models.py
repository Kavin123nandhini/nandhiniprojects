from django.db import models
from app_restapi.models import UserRegistration
from django.contrib.auth.models import User


# Create your models here.


class Friends(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             related_name='user_friendships')
    friend = models.ForeignKey(User, on_delete=models.CASCADE,
                               related_name='friend_friendships')
    status = models.CharField(max_length=50, default='pending')
    request_date = models.DateTimeField(auto_now_add=True)


    # Other fields related to the friendship...

    # def __str__(self):
    #     return f"{self.user.username} -> {self.friend.username}"

    def accept(self):
        self.status = 'accepted'
        self.save()


class Messages(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE,
                               related_name='sender')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE,
                                 related_name='receiver')
    # storing paragraphs and all other text data
    content = models.TextField(max_length=10000)
    timestamp = models.DateTimeField(auto_now_add=True)
    is_public = models.BooleanField(default=False)  # Add this field

    def __str__(self):
        return f'{self.sender} to {self.receiver} - {self.timestamp}'


class JobListing(models.Model):
    title = models.CharField(max_length=100,blank=True,null=True)
    description = models.TextField(max_length=1000,blank=True,null=True)
    skills_req= models.CharField(max_length=500,blank=True,null=True)
    job_type = models.CharField(max_length=100,blank=True,null=True)
    posted_by = models.ForeignKey(User, on_delete=models.CASCADE,
                                  related_name="joblisting")
    posted_date = models.DateTimeField(auto_now_add=True)


class JobAppliedUser(models.Model):
    job = models.ForeignKey(JobListing, on_delete=models.CASCADE,
                            related_name="job")
    applied_user = models.ForeignKey(User, on_delete=models.CASCADE,
                                     related_name="applied_user")
    remarks = models.CharField(max_length=100, default="pending")
    created_at = models.DateTimeField(auto_now_add=True)
    submit_resume=models.FileField(upload_to="resume/",blank=True,null=True)
