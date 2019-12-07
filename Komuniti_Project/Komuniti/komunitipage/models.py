from django.contrib.auth.models import User
from django.db import models
from django.contrib.postgres.fields import HStoreField, JSONField


# Create your models here.


class Community(models.Model):
    title = models.CharField(max_length=120, unique=True)
    description = models.TextField(blank=True)
    # TODO: Community Yaratmak için bir form olması lazım. Bu formun altında add datatypes gelmesi lazım
    image = models.ImageField(upload_to='community_thumbnail', default='community_thumbnail/no-img.jpg')

    # another_info = models.CharField(max_length=10, blank=True)
    #,

    def __str__(self):
        return self.title


class FormField(models.Model):
    # Constants for generic string types
    IMAGE = 'IM'
    VIDEO = 'VI'
    AUDIO = 'AU'
    TEXT = 'TE'
    TEXT_AREA = 'TA'
    URI = 'UR'
    LOCATION = 'LO'
    DATE = 'DA'
    DECIMAL = 'DE'
    INT = 'IM'
    Generic_Field_Types = (
        (IMAGE, 'Image'),
        (VIDEO, 'Video'),
        (AUDIO, 'Audio'),
        (TEXT, 'Text field'),
        (TEXT_AREA, 'Text area'),
        (URI, 'URI'),
        (LOCATION, 'Location'),
        (DATE, 'Date'),
        (DECIMAL, 'Decimal'),
        (INT, 'Integer')
    )
    community = models.ForeignKey(Community, default="", on_delete=models.CASCADE)
    field_type = models.CharField(max_length=2, choices=Generic_Field_Types, default=TEXT)
    field_label = models.CharField(max_length=50)
    is_required = models.BooleanField(default=False)

    def __str__(self):
        return self.field_label


class DataType(models.Model):
    # Burası tamam gibi
    name = models.CharField(max_length=200)
    community = models.ForeignKey(Community, on_delete=models.PROTECT)
    # fields = JSONField(blank=True)
    # fields = models.ManyToManyField(FormField)
    data_field = JSONField(db_index=True, blank=True)
    is_required = models.BooleanField(db_index=True, default=True)

    #def __str__(self):
    #    template =  '{0.name}:{0.data_field}'
    #    return template.format(self)

    def __str__(self):
        return self.name

    #def publish(self):
    #    self.data_field


class Post(models.Model):
    community = models.ForeignKey(Community, models.CASCADE)
    title = models.CharField(max_length=120, unique=True)
    description = models.TextField(blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)

    # data_field = models.ForeignKey(DataField,on_delete=models.CASCADE, default=1)
    # real_field_data = HStoreField(db_index=True, blank=True)

    # TODO: Needs to get the Data Fields of one community
    post_data = JSONField(default="")

    # extra_fields = HStoreField(db_index=True)

    def __str__(self):
        return self.title
    # image = models.ImageField()


class CommunityTag(models.Model):
    tag_desc = models.CharField(max_length=100)
    community = models.ForeignKey(Community, default="", on_delete=models.CASCADE)
    tag_info = JSONField(default="")
