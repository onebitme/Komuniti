import datetime
import random
import string

from django.contrib.auth import authenticate , login, logout
from django.core.serializers.json import DjangoJSONEncoder
from django.http import HttpResponse, HttpResponseForbidden, JsonResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, render_to_response, redirect
from django.template import RequestContext
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt

from .forms import CustomForm, PostForm, ImageUploadForm
# from djangojsonschema.jsonschema import DjangoFormToJSONSchema
from django.contrib.postgres.fields import JSONField
from django.core import serializers
from rest_framework import viewsets
from django.core.serializers import serialize
from django.contrib.auth.models import User, Group

import requests
from .models import *
import json

'''
Code Revisit: 
removed def's:
1-Lazy Encoder
2- communities
3- post_new
4- community_search
5- random_string generator  
'''
def home(request):

    if request.user.is_authenticated:
        logstatus = "Yes"
        community = Community.objects
        print('oldu bu iş')
        if request.method == 'GET':  # If the form is submitted
            search_query = request.GET.get('search_community')
            if search_query != "" and search_query != None:
                community = Community.objects.filter(title__icontains=search_query)
            elif search_query != "" and search_query != None:
                community = Community.objects.filter(description__icontains=search_query)
            else:
                community = Community.objects.all()
    else:
        logstatus = "You are not logged in Kommy, Log in Kommy"
        community = None

    return render(request, 'komunitipage/home.html', {'communities': community , 'logstatus' : logstatus})

#TODO When Communities field is Not filled, no search
def advancedSearch(request):
    if request.user.is_authenticated:
        tags = ""
        posts = ""
        communities = ""
        community_query = "böyle de bir şey yoktur"


        if request.method == 'POST':
            community_query = request.POST['community_search']
            post_query = request.POST['post_search']
            tags_query = request.POST['tag_search']
            #No Form with Search Info
            if community_query =="" and post_query == "" and tags_query == "":
                print("tam boş search")
                return render(request, 'komunitipage/advancedSearch.html',{'tags':tags,'posts':posts,'communities': communities})
            #Only Community Search
            elif community_query !="" and post_query == "" and tags_query == "":
                communities = Community.objects.filter(title__icontains=community_query)
                print("sadece community search")
                return render(request, 'komunitipage/advancedSearch.html', {'tags': tags, 'posts': posts, 'communities': communities})
            #TODO: Only Tags Search & Tags of community combined
            elif community_query != "" and post_query == "" and tags_query != "":
                communities = Community.objects.filter(title__icontains=community_query)
                community_list = list()
                another_f = {}
                another_f['fields'] = []
                for community in communities:
                    community_list.append(community)
                for i in range(len(community_list)):
                    tags_json=community_list[i].tags['fields']
                    for key in tags_json:
                        #TODO: No Case sensitive
                        if tags_query in key['tag']:
                            another_f['fields'].append(
                                {
                                    "Q": key['Q'],
                                    "tag": key['tag']
                                }
                            )
                return render(request, 'komunitipage/advancedSearch.html',
                              {'tags': another_f})

            #Only Post Search
            elif community_query =="" and post_query != "" and tags_query == "":
                posts = Post.objects.filter()
                post_list = list()
                for post in posts:
                    post_list.append(post)

                another_f = {}
                another_f['fields'] = []
                id = 1

                for key in post_list:
                    for i in key.post_data['fields']:
                        if post_query in i['values']:
                            another_f['fields'].append(
                                {
                                "fields": key.post_data['fields'],
                                "post_id": key.pk
                                }
                            )

                print("Sadece Post Searchteyiz")
                return render(request, 'komunitipage/advancedSearch.html',{'tags': tags, 'post': another_f, 'communities': communities})
            #Inside Community Post Search // Included the error handling for this case
            elif community_query !="" and post_query != "" and tags_query == "":
                communities = Community.objects.filter(title__icontains=community_query)
                if len(communities) > 0:
                    community_list=list()
                    for community in communities:
                        community_list.append(community)
                        posts = Post.objects.filter(community=community)
                        if len(posts)>0:
                            post_list = list()
                            for post in posts:
                                post_list.append(post)

                            another_f = {}
                            another_f['fields'] = []

                            for key in post_list:
                                 for i in key.post_data['fields']:
                                    if  post_query in i['values']:
                                        another_f['fields'].append(
                                            {
                                            "fields": key.post_data['fields'],
                                            "post_id": key.pk
                                            }
                                        )
                            if len(another_f['fields'])<1:
                                print(another_f)
                                message = "No Posts as: " + post_query + " under Community: " + community.title
                                return render(request, 'komunitipage/advancedSearch.html', {'post': another_f,'message': message})
                            return render(request, 'komunitipage/advancedSearch.html',{'post': another_f})
                        else:
                            message = "No Posts under Community: " + community.title
                            print(message)
                            return render(request, 'komunitipage/advancedSearch.html', {'message': message})
                else:
                    message = "No Community Exists"
                    return render(request, 'komunitipage/advancedSearch.html', {'message': message})

        else:
            print("Post olmadı")

        return render(request, 'komunitipage/advancedSearch.html', {'tags':tags,'posts':posts,'communities': communities})
    else:
        community = 0
        naughty = "Trying Random HTMLs Kommy?"
        return render(request, 'komunitipage/home.html', {'communities': community , 'logstatus' : naughty})

#TODO: No ENUM
def add2Community(request ,communityId):
    if request.user.is_authenticated:
        if request.method == "POST":
            query = CustomForm(request.POST)
            ##https://docs.djangoproject.com/en/2.2/ref/models/instances/
            if query.is_valid():
                print('--------------------------')
                # With this line, it transforms the form from HTML to JsonSchema
                cleaned_query = query.cleaned_data['data_type']
                print(cleaned_query)
                data_type_object = DataType()
                community = Community.objects.get(id=communityId)
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
        return render(request, 'komunitipage/add2Community.html', {'form': CustomForm, 'comid':communityId})
    else:
        community = 0
        naughty = "Trying Random HTMLs Kommy?"
        return render(request, 'komunitipage/home.html', {'communities': community , 'logstatus' : naughty})

#TODO: There is no post type, TRY to add it.
def add_post(request, communityId):
    if request.user.is_authenticated:
        community = get_object_or_404(Community, id=communityId)
        query = DataType.objects.filter(community=community)
        data_types = {}
        data_types['names'] = []
        data_types['field_type'] = []
        for i in range(len(query)):
            print(query[i].name)
            data_types['names'].append(query[i].name)
            data_types['field_type'].append(query[i].data_field)
        f = {}
        f['fields'] = []
        for key in range(len(data_types['names'])):
            field_name = data_types['names'][key]
            field_type = data_types['field_type'][key]
            f['fields'].append(
                {
                "name": field_name,
                "field_type":field_type
            }
            )
        post_json = {}
        post_json['fields']=[]
        if request.method == "POST":
            #print(request.POST)
            query = request.POST
            print(query)

            _mutable = query._mutable
            query._mutable = True
            del query['csrfmiddlewaretoken']
            query._mutable= False
            #TODO: OLM RANDOMU DUZELT.
            pk_rand= random.randint(0,2800);
            i=0
            post_object = Post(community=community, post_data=post_json, pk=pk_rand)
            for key,value in query.items():
                print(key,value)

                #This portion of the code is a modified version of the:
                # https://github.com/batidibek/VirCom/blob/development/vircom/views.py
                # Comit Number: 9bc0139
                if key == "Image":
                    user_file=""
                    image_file= ImageFile(upload=user_file, url="")
                    image_url = list(image_file.upload.name)
                    counter = 0
                    for key in image_url:
                        if key ==" ":
                            image_url[counter] = "_"
                        counter = counter + 1
                    image_url = ''.join(image_url)
                    image_file.url = image_url
                    image_file.save()
                    value = "gallery/" + image_url
                    print("buraya geldin")
                else:
                    print("kaydedemedin")

                post_json['fields'].append({
                    "data_names": key,
                    "values": value,
                    "data_type": data_types['field_type'][i],
                    "post_id" : post_object.pk
                })
                i +=1

            post_object.save()
        else:
            print(1111)
        return render(request, 'komunitipage/add_post.html', {'form_2':f ,'comid':communityId})
    else:
        community = 0
        naughty = "Trying Random HTMLs Kommy?"
        return render(request, 'komunitipage/home.html', {'communities': community , 'logstatus' : naughty})



#TODO: NO Edit
def view_community(request, communityId):
    if request.user.is_authenticated:
        Community_detail = get_object_or_404(Community,id=communityId)

        query_post = Post.objects.filter(community = Community_detail)
        post_list = list()

        for post in query_post:
            post_list.append(post)

        another_f = {}
        another_f['fields'] = []
        id = 1

        for key in post_list:
            another_f['fields'].append(
                {
                    "fields" : key.post_data['fields'],
                    "post_id": key.pk
                }
            )
            id +=1
        print(another_f)
        print(Community_detail.tags)

        return render(request,'komunitipage/view_community.html',{'community': Community_detail, 'comid':communityId , 'post':another_f, 'comtags':Community_detail.tags})
    else:
        community = 0
        naughty = "Trying Random HTMLs Kommy?"
        return render(request, 'komunitipage/home.html', {'communities': community , 'logstatus' : naughty})
#TODO: NO Edit
def view_post(request, postId):
    if request.user.is_authenticated:
        post = Post.objects.get(id=postId)
        communityId = post.community.pk
        post_data = post.post_data
        print(post_data)
        print("*****----*****")
        another_f = {}
        another_f['fields'] = []

        another_f['fields'].append(
            {
                "fields": post_data['fields'],
            }
        )
        print(another_f)
        return render(request,'komunitipage/view_post.html', {'post': another_f, 'comid':communityId})
    else:
        community = 0
        naughty = "Trying Random HTMLs Kommy?"
        return render(request, 'komunitipage/home.html', {'communities': community , 'logstatus' : naughty})

#TODO: Does not Upload.
def upload_pic(request):
    if request.method == 'POST':
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            m = Community.image
            m.model_pic = form.cleaned_data['image']
            m.save()
            return HttpResponse('image upload success')
    return HttpResponseForbidden('allowed only via POST')

#After community is created, community builder needs to add the tags
#TODO: NO Edit
def create_community(request):
    if request.user.is_authenticated:
        community = Community()
        if request.method == "POST":
            query = request.POST

            community.title=query['community_title']
            community.description = query['community_description']
            community.tags = {}
            community.tags['fields'] = []
            community.date_pub = datetime.datetime.now()
            print(community.title + "*****" + community.description)
            community.save()

            return redirect("/")
        else:
            return render(request, "komunitipage/create_community.html", {})

        return render(request, 'komunitipage/create_community.html')
    else:
        community = 0
        naughty = "Trying Random HTMLs Kommy?"
        return render(request, 'komunitipage/home.html', {'communities': community , 'logstatus' : naughty})

#TODO: Bundan bir tane de postlar için yap
def searchTagCom(request, communityId):
    if request.user.is_authenticated:
        r_json = {}
        community = Community.objects.get(id=communityId)
        print(community.tags)

        if request.POST:
            if request.POST['search_results']:
                API_ENDPOINT = "https://www.wikidata.org/w/api.php"
                query = request.POST['search_results']
                #query.replace(" ", "&")

                params = {
                    'action': 'wbsearchentities',
                    'format': 'json',
                    'language': 'en',
                    'limit': '5',
                    'search': query
                }
                wiki_request = requests.get(API_ENDPOINT, params=params)
                r_json = wiki_request.json()['search']
                r_json = json.dumps(r_json)
                r_json = json.loads(r_json)
                print(r_json)
            elif request.POST['selectq'] and request.POST['tags']:
                selectq = request.POST.get('selectq')
                tag = request.POST['tags']
                community.tags['fields'].append(
                    {
                        "Q": selectq,
                        "tag": tag
                    }
                )
                community.save()
            else:
                return render(request, 'komunitipage/searchTag.html', {'r_json': r_json, 'comid':communityId})
        return render(request, 'komunitipage/searchTag.html', {'r_json': r_json,'comid':communityId})
    else:
        community = 0
        naughty = "Trying Random HTMLs Kommy?"
        return render(request, 'komunitipage/home.html', {'communities': community , 'logstatus' : naughty})


def log_in(request):
    return render(request, 'komunitipage/login.html')


def authenticated_user(request):
    if request.POST:
        username = request.POST['username']
        password = request.POST['password']
        if username=="" or password == "":
            return render(request, 'komunitipage/login.html', {'message': "Empty Fields You Got There!"})
        user = authenticate(request, username=username, password = password)
        print(username)
        if user is None:
            return render(request, 'komunitipage/login.html', {'message': "Wrong Credentials My fellow Kommy"})
        elif user is not None:
            login(request, user)
            return home(request)

def log_out(request):
    logout(request)
    return render(request, 'komunitipage/logout.html')


