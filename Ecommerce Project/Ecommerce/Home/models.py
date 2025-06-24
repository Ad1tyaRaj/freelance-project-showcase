from django.db import models
from django.contrib.auth.models import User


# Create your models here.

class Newsletter(models.Model):
    email = models.EmailField()
    created_at = models.DateTimeField(auto_now_add=True)