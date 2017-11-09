# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse

def default(request):
    context= {
    }
    return render(request, 'base.html', context)

def guest_page(request):
    context={}
    return render(request, 'guest_page.html', context)

def projects_page(request):
    context={}
    return render(request, 'projects.html', context)

def contact_page(request):
    context={}
    return render(request, 'contact.html', context)
