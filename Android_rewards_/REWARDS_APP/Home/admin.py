from django.contrib import admin
from .models import AndroidApp, UserTask

# Register your models here.

@admin.register(AndroidApp)
class AndroidAppAdmin(admin.ModelAdmin):
    list_display = ('id','name', 'logo', 'download_link', 'package_name', 'points')

@admin.register(UserTask)
class UserTaskAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'screenshot', 'status')