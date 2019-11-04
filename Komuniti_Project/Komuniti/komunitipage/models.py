from django.db import models

# Create your models here.

class Community(models.Model):
    title = models.CharField(max_length=120, unique=True)
    description = models.TextField(blank=True)
    #image = models.ImageField(upload_to)