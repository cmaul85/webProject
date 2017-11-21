# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib.auth.models import User
from django.db import models
from django import forms
from django.db.models.signals import post_save
from django.dispatch import receiver


# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
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
        instance.profile.save()
    """

"""
class Projects(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=80, blank=False)
    rating = models.PositiveIntegerField(blank=True, default=0)
    number_of_ratings = models.PositiveIntegerField(blank=True, default=0)
    git_hub_link = models.URLField(blank=True, null=True, max_length=2000)

class Comments(models.Model):
    project = models.OneToOneField(Projects, on_delete=models.CASCADE)
"""
