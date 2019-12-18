import datetime
import random
import string

from django.core.serializers.json import DjangoJSONEncoder
from django.http import HttpResponse, HttpResponseForbidden, JsonResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, render_to_response, redirect
from django.template import RequestContext
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


def communities(request, userid):
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


#TODO: Postlar için random isimler alıyorsun.
def randomString(stringLength=10):
    """Generate a random string of fixed length """
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(stringLength))



#TODO: Bunun enum desteklemesi gerekiyor
def add2Community(request ,communityId):
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

def add_post(request, communityId):
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
                "field_type": field_type
            }
        )

    post_json = {}
    post_json['fields'] = []

    if request.method == "POST":
        # print(request.POST)
        query = request.POST
        print(query)

        _mutable = query._mutable
        query._mutable = True
        del query['csrfmiddlewaretoken']
        query._mutable = False
        pk_rand = random.randint(0, 2800);
        i = 0
        post_object = Post(community=community, post_data=post_json, pk=pk_rand)
        for key, value in query.items():
            print(key, value)
            post_json['fields'].append({
                "data_names": key,
                "values": value,
                "data_type": data_types['field_type'][i],
                "post_id": post_object.pk
            })
            i += 1

        post_object.save()

    else:
        print(1111)

    # print(context)
    # post.post_data = data_types
    # post.save()

    return render(request, 'komunitipage/show_datatype.html', {'form_2': f})


#TODO: Postlar Geliyor, Ama Value'su ne falan, formun içinde eksik
def view_community(request, communityId):
    Community_detail = get_object_or_404(Community,id=communityId)

    query_post = Post.objects.filter(community = Community_detail)
    post_list = list()

    query_tags = CommunityTag.objects.filter(community = Community_detail)
    tag_list = list()

    for post in query_post:
        post_list.append(post)

    for tag in query_tags:
        tag_list.append(tag)

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

    return render(request,'komunitipage/view_community.html',{'community': Community_detail, 'comid':communityId , 'post':another_f })


#Bunu Silme
def view_post(request, postId):
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


#TODO: BUNU SİL
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

#TODO: TAG YOK
def create_community(request):
    community = Community()
    if request.method == "POST":
        query = request.POST
        #######################
        '''API_ENDPOINT = "https://www.wikidata.org/w/api.php"
        query_tags = request.POST['search_results']
        #query.replace(" ", "&")


        params = {
            'action': 'wbsearchentities',
            'format': 'json',
            'language': 'en',
            'limit': '3',
            'search': query_tags
        }
        wiki_request = requests.get(API_ENDPOINT, params=params)
        r_json = wiki_request.json()['search']
        r_json = json.dumps(r_json)
        r_json = json.loads(r_json)'''

        community.title=query['community_title']
        community.description = query['community_description']
        community.tags = {}
        community.date_pub = datetime.datetime.now()
        print(community.title + "*****" + community.description)
        community.save()

        return redirect("/")
    else:
        return render(request, "komunitipage/create_community.html", {})

    return render(request, 'komunitipage/create_community.html')

#TODO: Somehow biraz tag geliyor.
def searchTagCom(request, communityId):
    r_json = {}
    community = Community.objects.get(id=communityId)

    if request.POST:
        if request.POST['search_results']:
            API_ENDPOINT = "https://www.wikidata.org/w/api.php"
            query = request.POST['search_results']
            #query.replace(" ", "&")

            params = {
                'action': 'wbsearchentities',
                'format': 'json',
                'language': 'en',
                'limit': '3',
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
            community.tags['Q_value'].append(selectq)
            community.tags['tag_name'].append(tag)
            community.save()


        else:
            return render(request, 'komunitipage/searchTag.html', {'r_json': r_json, 'comid':communityId})
    return render(request, 'komunitipage/searchTag.html', {'r_json': r_json,'comid':communityId})

