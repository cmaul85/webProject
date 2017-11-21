# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib.auth.models import User
from django.db import models
from django import forms
from django.db.models.signals import post_save
from django.dispatch import receiver
import os


# Putting some helpful functions

# Create your models here.

class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    profile_image = models.ImageField(blank=True, upload_to='profile_images/', default='profile_images/generic_profile.jpg')
    git_hub_link = models.URLField(blank=True, null=True, max_length=2000)
    linkedin_link = models.URLField(blank=True, null=True, max_length=2000)


    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)

    """
    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, **kwargs):
        instance.Profile.save()
    """


class Projects(models.Model):
    project_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, unique=False, on_delete=models.CASCADE)
    name = models.CharField(max_length=80, blank=False)
    rating = models.PositiveIntegerField(blank=True, default=0)
    number_of_ratings = models.PositiveIntegerField(blank=True, default=0)
    git_hub_link = models.URLField(blank=True, null=True, max_length=2000)
    date = models.DateField(auto_now=False, auto_now_add=True)
    
"""
class Comments(models.Model):
    comment_id = models.AutoField(primary_key=True)
    project = models.ForeignKey(Projects, unique=False, on_delete=models.CASCADE)
    user = models.ForeignKey(User, unique=False, on_delete=models.CASCADE)
    date = models.DateField(auto_now=False, auto_now_add=True)
    comment = models.CharField(max_length=200)
    rating = models.PositiveIntegerField(blank=True, default=0)
"""


def generate_project_file_path(self, filename):
    name = self.project.user.username + '/'
    project_name = self.project.name + '/' + self.image.name + '/' 
    print(str('projects/' + name + project_name))
    return str('projects/' + name + project_name)


class Images(models.Model):
    image_id = models.AutoField(primary_key=True)
    project = models.ForeignKey(Projects, unique=False, on_delete=models.CASCADE)
    image = models.ImageField(blank=True, upload_to=generate_project_file_path)








