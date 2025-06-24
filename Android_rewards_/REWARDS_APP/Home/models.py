from django.db import models
from django.contrib.auth.models import User


# Create your models here.

class AndroidApp(models.Model):
    name = models.CharField(max_length=255)
    package_name = models.CharField(max_length=255, unique=True)
    logo = models.ImageField(upload_to="app_logos/")
    download_link = models.URLField()
    points = models.IntegerField()
    
    


class UserTask(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    screenshot = models.ImageField(upload_to="task_screenshots/")
    status = models.CharField(max_length=20, choices=[('pending', 'Pending'), ('approved', 'Approved')], default='pending')
