from django.conf.urls import url

from django.conf.urls import url, include
from django.contrib import admin
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
      url(r'^$', views.default, name='default'),
]


