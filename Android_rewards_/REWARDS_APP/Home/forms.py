from tabnanny import check
from django import forms
from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth.models import User
from .models import AndroidApp


class EditProfileForm(UserChangeForm):
    class Meta:
        model = User
        fields = '__all__'
        widgets = {
            'is_active': forms.Select(choices=((True, 'No'), (False, 'Yes'))),
        }   
        labels = {
            'username': 'Username',
            'first_name': 'First Name',
            'last_name': 'Last Name',
            'email': 'Email',
            'is_active': 'Is Active',
            'date_joined': 'Date Joined',
            'last_login': 'Last Login',
            'password': 'Password',
            'groups': 'Groups',
            'user_permissions': 'User Permissions',
            'is_staff': 'Is Staff',
            'edit': 'Edit',
            'save': 'Save'
        }


class AddTaskForm(forms.ModelForm):
    class Meta:
        model = AndroidApp
        fields = ['name', 'package_name', 'logo', 'download_link', 'points']
        labels = {
            'name': 'App Name',
            'package_name': 'Package Name',
            'logo': 'Logo',
            'download_link': 'Download Link',
            'points': 'Points'
        }