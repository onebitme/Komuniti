from django import forms

from .models import Post, Community, DataType
from django.forms import ModelForm, Form
from splitjson.widgets import SplitJSONWidget
from django_jsonforms.forms import JSONSchemaField

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
            "enum": ["String", "Integer", "Boolean", "Image", "Date", "Time","Enum","Location"]
        },
        "is required": {
            "type": "string",
            "enum": ["True", "False"]

        }

    }
}
options = {"no_additional_properties": True}


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('user', 'community', 'post_data')


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

#class ShowForm(forms.Form):



class ImageUploadForm(forms.Form):
    """Image upload form."""
    image = forms.ImageField()


class AddCommunity(forms.Form):
    Community_Name = forms.CharField()
    Community_Description = forms.CharField(
        widget=forms.Textarea(attrs={'width': "50%", 'cols': "50", 'rows': "2", }))
    Community_Tags = forms.CharField(widget=forms.Textarea(attrs={'width': "50%", 'cols': "50", 'rows': "2", }))
    Community_Image = forms.ImageField()
    Private_Community = forms.BooleanField(initial=False, required=False)

    def __init__(self, *args, **kwargs):
        super(AddCommunity, self).__init__(*args, **kwargs)
        self.fields['Community_Name'].label = "Community Name"
        self.fields['Community_Name'].widget.attrs.update({
            'class': 'form-control',
            "name": "Community Name"})
        self.fields['Community_Description'].label = "Community Description"
        self.fields['Community_Description'].widget.attrs.update({
            'class': 'form-control',
            "name": "Community Description"})
        self.fields['Community_Tags'].label = "Community Tags"
        self.fields['Community_Tags'].widget.attrs.update({
            'class': 'form-control',
            "name": "Community Tags"})

    def clean(self, *args, **keyargs):
        Community_Name = self.cleaned_data.get("Community Name")
        Community_Description = self.cleaned_data.get("Community Description")
        Community_Tags = self.cleaned_data.get("Community Tags")
        Community_Image = self.cleaned_data.get("Community Image")
        return super(AddCommunity, self).clean(*args, **keyargs)
