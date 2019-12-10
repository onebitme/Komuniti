import datetime
import random
import string

from django.core.serializers.json import DjangoJSONEncoder
from django.http import HttpResponse, HttpResponseForbidden, JsonResponse
from django.shortcuts import render, get_object_or_404, render_to_response, redirect
from django.template import RequestContext
from django.views.decorators.csrf import csrf_exempt

from .forms import CustomForm, PostForm, ImageUploadForm #ShowForm, AddCommunity
# from djangojsonschema.jsonschema import DjangoFormToJSONSchema
from django.contrib.postgres.fields import JSONField
from django.core import serializers
from rest_framework import viewsets
from django.core.serializers import serialize
from django.contrib.auth.models import User, Group

# from .forms import PostForm
import requests
from .models import *
from .services import CommunityService, WikidataService
import json


class LazyEncoder(DjangoJSONEncoder):
    def default(self, obj):
        if isinstance(obj, 'json'):
            return str(obj)
        return super().default(obj)


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

#TODO: Bunun enum desteklemesi gerekiyor
def add_datatype(request):
    if request.method == "POST":
        query = CustomForm(request.POST)
        ##https://docs.djangoproject.com/en/2.2/ref/models/instances/
        if query.is_valid():
            print('--------------------------')
            # With this line, it transforms the form from HTML to JsonSchema
            cleaned_query = query.cleaned_data['data_type']
            print(cleaned_query)
            data_type_object = DataType()
            community = Community.objects.get(title='Book Lovers')
            data_type_object.community = community
            data_type_object.name = cleaned_query['Data Field Name']
            data_type_object.data_field = cleaned_query['Data Field Type']
            if cleaned_query['is required'] == "True":
                data_type_object.is_required = True
            else:
                data_type_object.is_required = False
            data_type_object.save()
            print(data_type_object)

        else:
            print(11111111111111111111111)

    return render(request, 'komunitipage/add_datatype.html', {'form': CustomForm})

#TODO: Postlar için random isimler alıyorsun.
def randomString(stringLength=10):
    """Generate a random string of fixed length """
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(stringLength))

#TODO: Bunun adı artık Show_datatype olmasın da sanki post diye değiştirilsin
#TODO: Kaydettiğin format herhangi bir JSON falan uyuyor mu baksana
def show_datatype(request):

        community = get_object_or_404(Community, title='Book Lovers')
        query_list = list(DataType.objects.values())


        data_types = {}
        data_types['names'] = []
        data_types['field_type'] = []

        f = {}
        f['fields'] = []

        for key in query_list:
            # print(key['name'])
            data_types['names'].append(key['name'])
            data_types['field_type'].append(key['data_field'])
            # print('-*-*-*-*-*-*-*-*-*')

        for key in range(len(data_types['names'])):
            field_name = data_types['names'][key].strip()
            field_type = data_types['field_type'][key]
            print(field_type)
            print("------")
            print(field_name)
            f['fields'].append(
                {
                "name": field_name,
                "field_type":field_type
            }
            )

        post_json = {}
        post_json['names'] = []
        post_json['values'] = []
        #print(f)
        if request.method == "POST":
            #print(request.POST)
            query = request.POST
            print(query)

            _mutable = query._mutable
            query._mutable = True
            del query['csrfmiddlewaretoken']
            query._mutable= False

            for key,value in query.items():
                print(key,value)
                post_json['values'].append(value)
                post_json['names'].append(key)
                print(post_json)
        else:
            print(1111)

        post_object = Post(community=community,title=randomString(10),description='Deneme_1',post_data=post_json)

        post_object.save()
        #print(context)
        #post.post_data = data_types
        #post.save()


        return render(request, 'komunitipage/show_datatype.html', {'form_2':f})


#TODO: Postların gelmesi
def view_community(request, communityId):
    Community_detail = get_object_or_404(Community,id=communityId)
    return render(request,'komunitipage/view_community.html', {'community': Community_detail})

def community_edit(request):
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
    return render(request, 'komunitipage/community_edit.html')


def upload_pic(request):
    if request.method == 'POST':
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            m = Community.image
            m.model_pic = form.cleaned_data['image']
            m.save()
            return HttpResponse('image upload success')
    return HttpResponseForbidden('allowed only via POST')


def create_community(request):
    community = Community()
    if request.method == "POST":
        query = request.POST
        print(query)
        print("*******0000********")
        ######
        #tagsJson = request.POST.get('tagsJson')
        #community_tag = CommunityTag()
        ##community_tag.community = community
        #community_tag.tag_info = tagsJson
        #community_tag.save()
        # deneme = WikidataService.query()
        # print(deneme)
        community.title=query['community_title']
        community.description = query['community_description']
        community.tags = {"":""}
        community.date_pub = datetime.datetime.now()
        print(community.title + "*****" + community.description)
        community.save()

        return redirect("/")
    else:
        return render(request, "komunitipage/create_community.html", {})

    return render(request, 'komunitipage/create_community.html')

