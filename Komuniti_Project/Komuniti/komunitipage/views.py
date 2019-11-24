from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from .forms import CustomForm, PostForm
from rest_framework import viewsets
from .serializers import UserSerializer, GroupSerializer
from django.contrib.auth.models import User, Group

# from .forms import PostForm
from .models import *
import json


def home(request):
    com = Community.objects.get(title='Book Lovers')
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

    post = Post.objects.get(title='My Favorite Book')

    return render(request, 'komunitipage/home.html', {'post': post})


def hello():
    return HttpResponse("Hello Bu Sadece bir HTTP Response")


def communities(request):
    community = "dummy"
    if request.method == 'GET':  # If the form is submitted
        search_query = request.GET.get('search_community', None)

        if search_query != None:
            community = Community.objects.filter(title__icontains=search_query)

        else:
            community = None
    print(community)
    return render(request, 'komunitipage/communities.html', {'community': community})


def post_new(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        form.save()
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

    if request.method =="POST":
        form = CustomForm()
        if form != None:
            print(form)
        else:
            print(1)

    return render(request, 'komunitipage/add_datatype.html', {'form': CustomForm()})
