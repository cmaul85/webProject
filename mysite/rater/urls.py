from django.conf.urls import url

from django.conf.urls import url, include
from django.contrib import admin
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
      url(r'^$', views.default, name='default'),
      url(r'^guest$', views.guest_page, name='guest_page'),
      url(r'^register$', views.register_page, name='register_page'),
      url(r'^login$', views.login_page, name='login_page'),
      url(r'^projects$', views.projects_page, name='projects_page'),
      url(r'^contact$', views.contact_page, name='contact_page'),
      url(r'^logout$', views.logout_view, name='logout_page'),
      url(r'^profile/[\s\S]*$', views.profile_page, name='profile_page'),
      url(r'^add-project$', views.add_project, name='add_project_page'),
      url(r'^.+$', views.error_page, name="401")
]


