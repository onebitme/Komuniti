from django.db import models

# Create your models here.

#class Community(models.Model):

class Community(models.Model):
    title = models.CharField(max_length=120, unique=True)
    description = models.TextField(blank=True)
    #another_info = models.CharField(max_length=10, blank=True)
    #image = models.ImageField(upload_to)

    def __str__(self):
        return self.title

class Post(models.Model):
        title = models.CharField(max_length=120, unique=True)
        description = models.TextField(blank=True)