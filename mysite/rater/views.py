# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render, redirect
from .forms import *
from django.contrib.auth import login, logout

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

    context= {'name': Namecheck(request)}
    return render(request, Pagecheck(request), context)
            

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
            print("not failed")
            return redirect('/')
        else:
            print("failed")
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


def logout_view(request):
    logout(request)
    return redirect('/')
