# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib.auth.models import User
from django.db import models
from django import forms
from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver
from django.core.exceptions import ValidationError
import os
from PIL import Image


# Putting some helpful functions

# Create your models here.

class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    profile_image = models.ImageField(blank=True, upload_to='profile_images/', default='profile_images/generic_profile.jpg')
    git_hub_username = models.CharField(blank=True, null=True, max_length=80)
    linkedin_username = models.CharField(blank=True, null=True, max_length=80)


    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)


class Projects(models.Model):
    project_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, unique=False, on_delete=models.CASCADE)
    description = models.TextField(max_length=1000)
    name = models.CharField(max_length=80, blank=False)
    rating = models.PositiveIntegerField(blank=True, default=0)
    number_of_ratings = models.PositiveIntegerField(blank=True, default=0)
    git_hub_link = models.URLField(blank=True, null=True, max_length=2000)
    tags = models.TextField(blank=True, max_length=1000)
    date = models.DateField(auto_now=False, auto_now_add=True)


class Comments(models.Model):
    comment_id = models.AutoField(primary_key=True)
    project = models.ForeignKey(Projects, unique=False, on_delete=models.CASCADE)
    profile = models.ForeignKey(Profile, unique=False, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now=False, auto_now_add=True)
    comment = models.CharField(max_length=280)
    rating = models.PositiveIntegerField(blank=True, default=5)


def generate_project_file_path(self, filename):
    name = self.project.user.username + '/'
    project_name = self.project.name + '/' + self.image.name + '/' 
    print(str('projects/' + name + project_name))
    return str('projects/' + name + project_name)


def val_image_ext(value):
    valid_image_extensions = ['.png', '.jpg', '.bmp']
    ext = os.path.splitext(value.name)[1]
    if ext not in valid_image_extensions:
        raise ValidationError(u'Error Message')


@receiver(pre_delete, sender=Comments)
def create_new_comment(sender, instance, using, **kwargs):  
    project = instance.project
    project.rating -= int(instance.rating)
    project.number_of_ratings -= 1
    project.save()


class Images(models.Model):
    image_id = models.AutoField(primary_key=True)
    project = models.ForeignKey(Projects, blank=True, unique=False, on_delete=models.CASCADE)
    image = models.ImageField(upload_to=generate_project_file_path, validators=[val_image_ext])


@receiver(post_save, sender=Comments)
def create_new_comment(sender, instance, created, **kwargs):
    if created:
        project = instance.project
        project.rating += int(instance.rating)
        project.number_of_ratings += 1
        project.save()










