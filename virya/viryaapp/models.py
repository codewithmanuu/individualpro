
from django.db import models
from django.contrib.auth.models import User
from datetime import datetime


# Create your models here.

class dmodel(models.Model):
    username=models.CharField(max_length=30)
    email=models.EmailField()
    password=models.CharField(max_length=30)

class profile(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    auth_token=models.CharField(max_length=100)
    is_verified=models.BooleanField(default=False)
    created_at=models.DateTimeField(auto_now_add=True)

class orthomodel(models.Model):
    image = models.FileField(upload_to="viryaapp/static/")
    name=models.CharField(max_length=30)
    country=models.CharField(max_length=30)
    state=models.CharField(max_length=30)
    city=models.CharField(max_length=30)
    qualification=models.CharField(max_length=30)
    specialisation=models.CharField(max_length=30)

class Room(models.Model):
    name=models.CharField(max_length=1000)

class Messages(models.Model):
    value=models.CharField(max_length=1000000000)
    date=models.DateTimeField(default=datetime.now,blank=True)
    room=models.CharField(max_length=10000000)
    user=models.CharField(max_length=10000000)