from django import forms

from .models import Post, Community, DataType
from django.forms import ModelForm, Form
from django_jsonforms.forms import JSONSchemaField
from splitjson.widgets import SplitJSONWidget



data_type_schema = {
     "$id": "https://example.com/person.schema.json",
     "$schema": "http://json-schema.org/draft-07/schema#",
     "title": "Community",
     "type": "object",
     "properties": {
         "Data Field Name": {
             "type": "string",
         },
         "Data Field Type": {
             "type": "string",
             "enum": ["String", "Integer", "Boolean", "Image"]
         },
         "is required": {
             "type": "string",
             "enum": [ "True", "False"]

         }

     }
 }
#data_type_schema = {}
options = {"no_additional_properties": True}


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'description', 'user', 'community', 'real_field_data')


# class CustomForm(Form):
#    data_type = JSONSchemaField(schema = data_type_schema, options = options)

# class DataForm(forms.ModelForm):
#     class Meta:
#         model = DataType
#         fields = JSONSchemaField(data_type_schema,options)


class CustomForm(forms.Form):
    data_type = JSONSchemaField(schema=data_type_schema, options=options)

# class MyForm(forms.ModelForm):
#     class Meta:
#         model = DataType
#     subfield = JSONSchemaField(schema=data_type_schema, options=options)

class testForm(forms.Form):
    attrs = {'class': 'special', 'size': '40'}
    data = forms.CharField(widget=SplitJSONWidget(attrs=attrs, debug=True))

class ImageUploadForm(forms.Form):
    """Image upload form."""
    image = forms.ImageField()
