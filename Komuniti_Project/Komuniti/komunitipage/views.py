from django.http import HttpResponse, HttpResponseForbidden
from django.shortcuts import render, get_object_or_404, render_to_response
from django.template import RequestContext

from .forms import CustomForm, PostForm, ImageUploadForm, testForm
# from djangojsonschema.jsonschema import DjangoFormToJSONSchema
from django.contrib.postgres.fields import JSONField
from django.core import serializers
from rest_framework import viewsets
from django.core.serializers import serialize
from django.contrib.auth.models import User, Group

# from .forms import PostForm
from .models import *
import json


def home(request):
    communities = Community.objects
    # Currently displays one title
    # post = Post.objects.get(title='')

    return render(request, 'komunitipage/home.html', {'communities': communities})


def communities(request):
    community = "dummy"
    if request.method == 'GET':  # If the form is submitted
        search_query = request.GET.get('search_community', None)

        if search_query != None:
            community = Community.objects.filter(title__icontains=search_query)

        else:
            community = None
    print(community)
    return render(request, 'komunitipage/community_.html', {'community': community})


def post_new(request):
    if request.method == "POST":
        form = PostForm(request.POST)
    else:
        form = PostForm()
    return render(request, 'komunitipage/community_edit.html', {'post': form})


def community_search(request):
    query = request.GET.get('search_community')
    template = 'komunitipage/home.html'
    community = Community.objects.filter(title__icontains=query)

    if request.method == 'GET':  # If the form is submitted
        search_query = request.GET.get('search_community', None)

        if search_query != None:
            community = Community.objects.filter(title__icontains=search_query)
        else:
            community = Community.objects.all()
    print(communities + '1')
    return render(request, template, {'community': community})


def add_datatype(request):

    if request.method == "POST":
        query = CustomForm(request.POST)
        ##https://docs.djangoproject.com/en/2.2/ref/models/instances/
        if query.is_valid():
            print('--------------------------')
            #With this line, it transforms the form from HTML to JsonSchema
            cleaned_query = query.cleaned_data['data_type']
            print(cleaned_query)
            data_type_object = DataType()
            community = Community.objects.get(title='Firefaytırs')
            data_type_object.community = community
            data_type_object.name = cleaned_query['Data Field Name']
            data_type_object.data_field = cleaned_query['Data Field Type']
            if cleaned_query['is required']=="True":
                data_type_object.is_required = True
            else:
                data_type_object.is_required = False
            data_type_object.save()

        else:
            print(11111111111111111111111)


    return render(request, 'komunitipage/add_datatype.html', {'form': CustomForm})


def dummy(request):
    com = Community.objects.get(title='Firefaytırs')
    value_list = list()
    value_list.append('top')
    value_list.append('True')
    extra_field_data = "{"
    i = 0

    for key, value in com.post_type.items():
        extra_field_data += "'" + key + "':" + "'" + value_list[i] + "',"
        i += 1

    extra_field_data = extra_field_data[:-1]
    extra_field_data += "}"
    extra_field_data = json.dumps(extra_field_data)
    print(extra_field_data)
    return HttpResponse()


def upload_pic(request):
    if request.method == 'POST':
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            m = Community.image
            m.model_pic = form.cleaned_data['image']
            m.save()
            return HttpResponse('image upload success')
    return HttpResponseForbidden('allowed only via POST')


