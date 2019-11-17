from django import forms

from .models import Post
from .models import Community

class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ('title', 'description','user','community')

class DataTypeForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = {}