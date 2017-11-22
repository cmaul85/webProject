from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django import forms
from .models import *


class Register_form(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)


    class Meta:
        model = User
        fields = (
                'username',
                'first_name',
                'last_name',                
                'email',
                'password1',
                'password2')

    def __init__(self, *args, **kwargs):
        super(Register_form, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'class': 'form-control'})
        self.fields['first_name'].widget.attrs.update({'class': 'form-control'})
        self.fields['last_name'].widget.attrs.update({'class': 'form-control'})
        self.fields['email'].widget.attrs.update({'class': 'form-control'})
        self.fields['password1'].widget.attrs.update({'class': 'form-control'})
        self.fields['password2'].widget.attrs.update({'class': 'form-control'})



    def save(self, commit=True):
        user = super(Register_form, self).save(commit=False)
        user.username = self.cleaned_data['username']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.email = self.cleaned_data['email']
        if commit:
            user.save()




class Login_form(AuthenticationForm):
    username = forms.CharField(label="Username", max_length=30, 
            widget=forms.TextInput(attrs={'class': 'form-control', 'name': 'username'}))
    password = forms.CharField(label="Password", max_length=30, 
            widget=forms.PasswordInput(attrs={'class': 'form-control', 'name': 'password'}))
    def validate(self, request):
        username = request.POST['username']
        password = request.POST['password']
        return authenticate(username=username, password=password)


class Edit_Profile_form(forms.ModelForm):
    profile_image = forms.ImageField(required=False)
    #linkedin_link = forms.URLField()
    #git_hub_link = forms.URLField()

    class Meta:
        model = Profile
        fields = (
                  'profile_image',
                  'git_hub_username',
                  'linkedin_username',
                  )
    def save(self, profile, commit=True):
        if self.cleaned_data['profile_image'] != None:
            profile.profile_image = self.cleaned_data['profile_image']
        profile.git_hub_username = self.cleaned_data['git_hub_username']
        profile.linkedin_username = self.cleaned_data['linkedin_username']
        if commit:
            profile.save()


class Edit_User_form(forms.ModelForm):
    class Meta:
        model = User
        fields = (
                  'first_name',
                  'last_name',
                  'email',
                  )
    def save(self, user, commit=True):
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.email = self.cleaned_data['email']
        if commit:
            user.save()





