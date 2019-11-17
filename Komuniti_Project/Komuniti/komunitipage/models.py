from django.contrib.auth.models import User
from django.db import models
from rest_framework import generics


# from rest_framework.


# Create your models here.


class Community(models.Model):
    title = models.CharField(max_length=120, unique=True)
    description = models.TextField(blank=True)

    # another_info = models.CharField(max_length=10, blank=True)
    # image = models.ImageField(upload_to)

    def __str__(self):
        return self.title


class Post(models.Model):
    title = models.CharField(max_length=120, unique=True)
    description = models.TextField(blank=True)
    community = models.ForeignKey(Community, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)

    def __str__(self):
        return self.title
    # image = models.ImageField()
