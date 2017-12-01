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
        
    def __init__(self, *args, **kwargs):
        super(Edit_Profile_form, self).__init__(*args, **kwargs)
        self.fields['profile_image'].widget.attrs.update({'class': 'form-control'})
        self.fields['git_hub_username'].widget.attrs.update({'class': 'form-control'})
        self.fields['linkedin_username'].widget.attrs.update({'class': 'form-control'})

    def save(self, profile, commit=True):
        if self.cleaned_data['profile_image'] != None:
            profile.profile_image = self.cleaned_data['profile_image']
            profile.profile_image_thumb = self.cleaned_data['profile_image']
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
    def __init__(self, *args, **kwargs):
        super(Edit_User_form, self).__init__(*args, **kwargs)
        self.fields['first_name'].widget.attrs.update({'class': 'form-control'})
        self.fields['last_name'].widget.attrs.update({'class': 'form-control'})
        self.fields['email'].widget.attrs.update({'class': 'form-control'})

    def save(self, user, commit=True):
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.email = self.cleaned_data['email']
        if commit:
            user.save()


class Add_Project_form(forms.ModelForm):
    name = forms.CharField(max_length=80)
    description = forms.CharField(widget=forms.Textarea)
    git_hub_link = forms.URLField(max_length=2000, required=False)

    class Meta:
        model = Projects
        fields = ('name',
                  'description',
                  'git_hub_link',
                 )
    def __init__(self, *args, **kwargs):
        super(Add_Project_form, self).__init__(*args, **kwargs)
        self.fields['name'].widget.attrs.update({'class': 'form-control'})
        self.fields['description'].widget.attrs.update({'class': 'form-control'})
        self.fields['git_hub_link'].widget.attrs.update({'class': 'form-control'})

    def save(self, user, tags, commit=True):
        print(tags)
        project = super(Add_Project_form, self).save(commit=False)
        project.user = user
        project.name = self.cleaned_data['name']
        project.description = self.cleaned_data['description']
        project.git_hub_link = self.cleaned_data['git_hub_link']
        if tags != None and tags != "":
            project.tags = tags
        if commit:
            project.save()
            return project


class Add_Image_form(forms.ModelForm):
    image = forms.ImageField(widget=forms.ClearableFileInput(attrs={'multiple':True}), required=True)
    class Meta:
        model = Images
        fields = ('image', )

    def __init__(self, *args, **kwargs):
        super(Add_Image_form, self).__init__(*args, **kwargs)
        self.fields['image'].widget.attrs.update({'class': 'form-control'})

    def save(self, project, commit=True):
        image = super(Add_Image_form, self).save(commit=False)
        image.project = project
        if commit:
            image.save()


class Add_Comment_form(forms.ModelForm):
    comment = forms.CharField(max_length=280)
    rating = forms.IntegerField(max_value=5, min_value=1, required=True)
    
    class Meta:
        model = Comments
        fields = ('comment', 'rating', )

    def save(self, project, profile, commit=True):
        new_comment = super(Add_Comment_form, self).save(commit=False)
        new_comment.project = project
        new_comment.profile = profile
        new_comment.comment = self.cleaned_data['comment']
        new_comment.rating = int(self.cleaned_data['rating'])
        if commit:
            new_comment.save()

















