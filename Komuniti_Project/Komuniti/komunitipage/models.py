from django.contrib.auth.models import User
from django.db import models
from django.contrib.postgres.fields import HStoreField, JSONField, ArrayField
from django.db.models import ImageField


class Community(models.Model):
    title = models.CharField(max_length=120, unique=True)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='community_thumbnail', default='community_thumbnail/no-img.jpg')
    tags = JSONField(blank=True, default={})
    date_pub = models.DateTimeField(blank=True)

    def __str__(self):
        return self.title

    def __int__(self):
        return self.id


class DataType(models.Model):
    name = models.CharField(max_length=200)
    community = models.ForeignKey(Community, on_delete=models.PROTECT)
    data_field = JSONField(blank=True)
    is_required = models.BooleanField(db_index=True, default=True)

    #def __str__(self):
    #    template =  '{0.name}:{0.data_field}'
    #    return template.format(self)

    def __str__(self):
        return self.name
    def __str__(self):
        return self.data_field
    def __int__(self):
        return self.community


class Post(models.Model):
    community = models.ForeignKey(Community, models.PROTECT)
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    post_data = JSONField(default="")


class ImageFile(models.Model):
    upload = models.ImageField(upload_to='gallery')
    url = models.TextField(blank = True)
    def __str__(self):
        return str(self.upload)


class CommunityUser(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    joined_communities = ArrayField(models.IntegerField(), blank=True, null=True)

    def __str__(self):
        return self.user
