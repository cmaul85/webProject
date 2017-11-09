# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render, redirect
from .forms import *
from django.contrib.auth import login

# Create your views here.
from django.http import HttpResponse

def default(request):
    context= {
    }
    return render(request, 'base.html', context)

def guest_page(request):
    context={}
    return render(request, 'guest_page.html', context)

def register_page(request):
    if (request.method == 'POST'):
        form = Register_form(request.POST)
        if form.is_valid():
            form.save(commit=True)
            return redirect('/')
    else:
        form = Register_form()

    content = {'form': form}
    return render(request, 'register_page.html', content)

def login_page(request):
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

    content = {'form': form}
    return render(request, 'login_page.html', content)
