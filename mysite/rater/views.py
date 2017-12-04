# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render, redirect
from .forms import *
from .models import *
from .python_scripts.py_scripts import *
from django.contrib.auth import login, logout
from django.contrib.auth.models import User


# Create your views here.
from django.http import HttpResponse

def Namecheck(request):
    if(request.user.is_authenticated):
        name= request.user.username
    else:
        name= "Guest"

    return name


def Pagecheck(request):
    if(request.user.is_authenticated):
        return "user_page.html"#needs to be user_page.html once created
    else:
        return "guest_page.html"


def default(request):

    context= {'name': Namecheck(request),
            'extend_val': Pagecheck(request)}
    return render(request, 'welcome.html', context)
            

#### this is for testing only. Nothing directs to /guest
def guest_page(request):
    if(not request.user.is_authenticated):
        register_text = "Register"
    else:
        register_text =""

    context={'name': Namecheck(request), 
            'register_text': register_text}
    return render(request, 'guest_page.html', context)


def register_page(request):
    if(request.user.is_authenticated):
        return redirect('/')
    if (request.method == 'POST'):
        form = Register_form(request.POST)
        if form.is_valid():
            form.save(commit=True)
            user = User.objects.get(username=request.POST['username'])
            login(request,user)
            return redirect('/')
    else:
        form = Register_form()

    content = {'form': form,
                'var': Pagecheck(request),
                'name': Namecheck(request)}
    return render(request, 'register_page.html', content)


def login_page(request):
    if(request.user.is_authenticated):
        return redirect('/')
    if (request.method == 'POST'):
        form = Login_form(request.POST)
        user = form.validate(request)
        if user is not None:
            login(request, user)
            return redirect('/')
        else:
            return redirect('/login')
    else:
        form = Login_form()
    content = {'form': form,
            'name': Namecheck(request)}
    return render(request, 'login_page.html', content)


def projects_page(request, search_results):
    project_list = get_porject_list(Projects.objects.all(), search_results)
    context={'name': Namecheck(request),
            'extend_val': Pagecheck(request),
            'project_object_list': project_list,}
    return render(request, 'projects.html', context)


def contact_page(request):
    context={'name': Namecheck(request),
            'extend_val': Pagecheck(request)}
    return render(request, 'contact.html', context)


def profile_page(request, user_profile):
    #user_profile = request.path_info.split('/')[len(request.path_info.split('/')) - 1]
    if request.method == 'GET':
        ## Check to see if user is valid
        if (not User.objects.filter(username=user_profile).exists()):
            return redirect('/')
        current_user = User.objects.get(username=user_profile)
        user_profile = Profile.objects.get(user=current_user)

        if request.user.username == user_profile.user.username:
            owners_profile_flag = True
            owners_profile_form = Edit_Profile_form(initial={
                                               #'profile_image': user_profile.profile_image, 
                                               'linkedin_username' : user_profile.linkedin_username,
                                               'git_hub_username' : user_profile.git_hub_username,
                                               })
            owners_user_form = Edit_User_form(initial={
                                               'first_name': current_user.first_name,
                                               'last_name' : current_user.last_name,
                                               'email' : current_user.email,
                                               })
        else:
            owners_profile_flag = False
            owners_profile_form = ""
            owners_user_form = ""

        # Logic on to show github and linkedin buttons and edit features
        current_flags = Get_flags(user_profile, owners_profile_flag)
            

        content = { "var": Pagecheck(request),
                    "name": Namecheck(request),
                    "current_flags" : current_flags,
                    "edit_profile_form" : owners_profile_form,
                    "edit_user_form" : owners_user_form,
                    "profile" : user_profile
                  }
        return render(request, 'profile_page.html', content)
    else:
        # this is when the method is a post when user edits profile.
        request.user.is_updating = ""
        user_obj = User.objects.get(username=user_profile)
        profile_obj = Profile.objects.get(user=user_obj)
        edit_user_form = Edit_User_form(request.POST)
        edit_profile_form = Edit_Profile_form(request.POST, request.FILES)
        if edit_profile_form.is_valid() and edit_user_form.is_valid():
            edit_profile_form.save(profile_obj)
            edit_user_form.save(user_obj)
            #print(request.path)
            return redirect(request.path)
        else:
            print(edit_profile_form.errors)
            return redirect('/error/')

def add_project(request):
    if request.user.is_authenticated:
        if request.method == 'GET':
            project_form = Add_Project_form()
            image_form = Add_Image_form()
            content = { "var": Pagecheck(request),
                        "name": Namecheck(request),
                        "project_form": project_form,
                        "image_form": image_form,
                      }
            return render(request, 'add_project_page.html', content)
        else:
            project_form = Add_Project_form(request.POST)
            images_form = Add_Image_form(request.POST, request.FILES)
            if project_form.is_valid():
                current_project = project_form.save(request.user, request.POST['tags'])
                for new_image in request.FILES.getlist('image'):
                    new_image_object = Images.objects.create(image=new_image,
                                                             project=current_project)
                return redirect('project/{}'.format(current_project.project_id))
            else:
                return redirect('/error/')
    else:
        return redirect('/')


# This is a customized comment object So I could match the url of each comment to Rating image.


def view_project_page(request):
    project_id = request.path_info.split('/')[len(request.path_info.split('/')) - 1]
    if request.method == 'GET':
        if not Projects.objects.filter(project_id=project_id).exists():
            return redirect('/')
        current_project = Projects.objects.get(project_id=project_id)
        images = Images.objects.filter(project=current_project)
        comment_list = Comments.objects.filter(project=current_project)
        new_comment_list = comment_list_converter(comment_list)
        comment_form = Add_Comment_form()
        project_rating = convert_project_rating(current_project)
        project_tags = current_project.tags.split(',')


        # If the user is logged in they need to be presented with comments
        if request.user.is_authenticated:
            current_flags = Get_flags(auth_flag=True)
        else:
            current_flags = Get_flags(auth_flag=False)
        

        content = { "var": Pagecheck(request),
                    "name": Namecheck(request),
                    "project": current_project,
                    "image_object": images,
                    "comment_list": new_comment_list,
                    "current_flags": current_flags,
                    "project_rating": project_rating,
                    "project_tags": project_tags,
                    "comment_form": comment_form,
                  }
        return render(request, 'individual_project_page.html', content)    
    else:
        # We could have a post from the owner of project editing project -or-
        # We could habe a post from Users adding comments.
        # Only one of these currently supported is Users adding comments.
        comment_form = Add_Comment_form(request.POST)
        current_project = Projects.objects.get(project_id=project_id)
        current_profile = Profile.objects.get(user=request.user)
        if comment_form.is_valid():
            comment_form.save(current_project, current_profile)
            return redirect(request.path)
        else:
            return redirect('/error/')



def error_page(request):
    return render(request, '401_page.html')


def logout_view(request):
    logout(request)
    return redirect('/')




"""
## Alternative method to validate if a user exist
try:
    current_user = User.objects.get(username=user_profile)
except:
    return redirect('/')
"""
