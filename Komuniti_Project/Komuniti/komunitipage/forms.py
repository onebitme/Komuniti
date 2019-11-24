from django import forms
from .models import Post, Community
from django.forms import ModelForm, Form
from django_jsonforms.forms import JSONSchemaField

data_type_schema = {
        "$id": "https://example.com/person.schema.json",
        "$schema": "http://json-schema.org/draft-07/schema#",
        "title": "Person",
        "type": "object",
        "properties": {
            "firstName": {
                "type": "string",
                "description": "The person's first name."
            },
            "lastName": {
                "type": "string",
                "description": "The person's last name."
            },
            "age": {
                "description": "Age in years which must be equal to or greater than zero.",
                "type": "integer",
                "minimum": 0
            }
        }
    }
options = {"no_additional_properties": True}


class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ('title', 'description','user','community','real_field_data')

class CustomForm(Form):
    data_type = JSONSchemaField(schema = data_type_schema, options = options)
