from django.contrib.auth.models import User
from django.db import models
from django.contrib.postgres.fields import HStoreField, JSONField




# Create your models here.


class Community(models.Model):
    title = models.CharField(max_length=120, unique=True)
    description = models.TextField(blank=True)
    post_type = HStoreField(db_index=True, blank=True)
    # another_info = models.CharField(max_length=10, blank=True)
    # image = models.ImageField(upload_to)

    def __str__(self):
        return self.title


class DataType(models.Model):
    name = models.CharField(max_length=200)
    community = models.ForeignKey(Community, on_delete=models.PROTECT)
    fields = JSONField()
    is_archived = models.BooleanField(default=False)
    def __str__(self):
        return self.name



class Post(models.Model):
    title = models.CharField(max_length=120, unique=True)
    description = models.TextField(blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    community = models.ForeignKey(Community, models.CASCADE)
    #data_field = models.ForeignKey(DataField,on_delete=models.CASCADE, default=1)
    real_field_data = HStoreField(db_index=True, blank=True)
    #extra_fields = HStoreField(db_index=True)


    def __str__(self):
        return self.title
    # image = models.ImageField()





