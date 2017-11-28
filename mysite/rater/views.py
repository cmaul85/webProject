# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render, redirect
from .forms import *
from .models import *
from django.contrib.auth import login, logout
from django.contrib.auth.models import User


# Create your views here.
from django.http import HttpResponse


class view_flags:
    def __init__(self, g_flag="", l_flag="", o_flag="", auth_flag=""):
        self.git_hub_flag = g_flag
        self.linkedin_flag = l_flag
        self.owners_profile_flag = o_flag
        self.is_authenticated = auth_flag

def Get_flags(user_profile=None, o_flag="", auth_flag=""):
    if user_profile is not None:
        if user_profile.git_hub_username not in [None, ""]:
            git_hub_flag = True
        else:
            git_hub_flag = False
        if user_profile.linkedin_username not in [None, ""]:
            linkedin_flag = True
        else:
            linkedin_flag = False
        return view_flags(g_flag=git_hub_flag, l_flag=linkedin_flag, o_flag=o_flag)
    else:
        return view_flags(auth_flag=auth_flag)


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


def projects_page(request):
    context={'name': Namecheck(request),
            'extend_val': Pagecheck(request)}
    return render(request, 'projects.html', context)


def contact_page(request):
    context={'name': Namecheck(request),
            'extend_val': Pagecheck(request)}
    return render(request, 'contact.html', context)


def profile_page(request):
    user_profile = request.path_info.split('/')[len(request.path_info.split('/')) - 1]
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
                current_project = project_form.save(request.user)
                for new_image in request.FILES.getlist('image'):
                    new_image_object = Images.objects.create(image=new_image,
                                                             project=current_project)
                return redirect('project/{}'.format(current_project.project_id))
            else:
                return redirect('/error/')
    else:
        return redirect('/')


# This is a customized comment object So I could match the url of each comment to Rating image.
class comment_object:
    def __init__(self, url, comment):
        self.rating_url = url
        self.comment = comment


def comment_list_converter(comment_list):
    new_comment_list = []
    pre_string = "/static/media/stars/"
    for i in comment_list:
        if i.rating == 1:
            temp_comment = comment_object("star_1.png", i)
        elif i.rating == 2:
            temp_comment = comment_object("star_2.png", i)
        elif i.rating == 3:
            temp_comment = comment_object("star_3.png", i)
        elif i.rating == 4:
            temp_comment = comment_object("star_4.png", i)
        elif i.rating == 5:
            temp_comment = comment_object("star_5.png", i)
        temp_comment.rating_url = pre_string + temp_comment.rating_url
        new_comment_list.append(temp_comment)
    return new_comment_list

# Use this function to get a rating out of the projects
def convert_project_rating(project):
    pre_string = "/static/media/stars/"
    if project.number_of_ratings == 0:
        return pre_string + "star_0.png"
    else:
        project_rating = project.rating / project.number_of_ratings
        if project_rating >= 1 and project_rating < 1.2:
            return pre_string + "star_1.png"
        elif project_rating >= 1.2 and project_rating < 1.8:
            return pre_string + "star_15.png"
        elif project_rating >= 1.8 and project_rating < 2.2:
            return pre_string + "star_2.png"
        elif project_rating >= 2.2 and project_rating < 2.8:
            return pre_string + "star_25.png"
        elif project_rating >= 2.8 and project_rating < 3.2:
            return pre_string + "star_3.png"
        elif project_rating >= 3.2 and project_rating < 3.8:
            return pre_string + "star_35.png"
        elif project_rating >= 3.8 and project_rating < 4.2:
            return pre_string + "star_4.png"
        elif project_rating >= 4.2 and project_rating < 4.8:
            return pre_string + "star_45.png"
        elif project_rating >= 4.8 and project_rating <= 5:
            return pre_string + "star_5.png"

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
