from django.contrib.auth.models import User
from django.db import models
from django.contrib.postgres.fields import HStoreField, JSONField


# Create your models here.


class Community(models.Model):
    title = models.CharField(max_length=120, unique=True)
    description = models.TextField(blank=True)
    post_type = HStoreField(db_index=True, blank=True)
    #TODO: Community Yaratmak için bir form olması lazım. Bu formun altında add datatypes gelmesi lazım
    image = models.ImageField(upload_to='community_thumbnail', default='community_thumbnail/no-img.jpg')

    # another_info = models.CharField(max_length=10, blank=True)
    #

    def __str__(self):
        return self.title



class DataType(models.Model):
    #Burası tamam gibi
    name = models.CharField(max_length=200)
    community = models.ForeignKey(Community, on_delete=models.PROTECT)
    # fields = JSONField(blank=True)
    data_field = JSONField(db_index=True, blank=True)
    is_required = models.BooleanField(db_index=True, default=True)

    def __str__(self):
        return self.name


class Post(models.Model):
    title = models.CharField(max_length=120, unique=True)
    description = models.TextField(blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    community = models.ForeignKey(Community, models.CASCADE)
    # data_field = models.ForeignKey(DataField,on_delete=models.CASCADE, default=1)
    real_field_data = HStoreField(db_index=True, blank=True)
    #TODO: Needs to get the Data Fields of one community
    # extra_fields = HStoreField(db_index=True)

    def __str__(self):
        return self.title
    # image = models.ImageField()
