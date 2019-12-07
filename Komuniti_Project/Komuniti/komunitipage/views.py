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


def show_datatype(request):
    '''community = Community.objects.get(title='Book Lovers')
    data_type = DataType(name=)
    # datatype = "{"
    #
    # for k in DataType.objects.filter(community=community):
    #     print(k)
    #     #datatype += serializers.serialize('json',data_field)
    #     #print(datatype)
    # print(datatype)


    # community = Community.objects.get(title='Book Lovers')
    # query = DataType.objects.filter(community=community)
    # datatypejson = serializers.serialize('json', query)
    # datatypejson = datatypejson[1:]
    # datatypejson = datatypejson[:-1]
    # datatypejson = json.dumps(datatypejson)
    # print(datatypejson)'''

    community = get_object_or_404(Community, title='Book Lovers')
    query_list = list(DataType.objects.values())
    # print(query_list)

    i = 0
    f = {}
    f['fields'] = []


    for key in query_list:
        print(key['name'])
        f['fields'].append(key['name'])
        print('-*-*-*-*-*-*-*-*-*')

        # extra_field_data=extra_field_data(key)

    print(f)
    # print(extra_field_data)
    # query_dict = dict(DataType.objects.values())
    # print(query_set)
    # datatypejson = serializers.serialize('json', query_set)
    # datatypejson = query_set
    # datatypejson = datatypejson[1:]
    # datatypejson = datatypejson[:-1]

    # query_list = json.loads(query_list)

    # context={ 'community' : community,
    #          'data_field' : data_field,
    #          'fields' : fields
    # }

    return render(request, 'komunitipage/show_datatype.html', {'form_2': key['name']})


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
    if request.method == "POST":
        community = Community
        community.title = request.POST.get("")
    return render(request, 'komunitipage/create_community.html')


# TODO: Not OK
@csrf_exempt
def new_community(request):
    if request.method == "POST":
        community = Community()
        community.title = request.POST.get("com_name", "")
        community.description = request.POST.get("com_description", "")
        # community.post_type = request.POST.get("com_post", "")
        community.save()
        # return HttpResponse(cmn.pk)

        tagsJson = request.POST.get('tagsJson')
        community_tag = CommunityTag()
        community_tag.community = community
        community_tag.tag_info = tagsJson
        community_tag.save()
        # deneme = WikidataService.query()
        # print(deneme)
        return redirect("/")
    else:
        return render(request, "komunitipage/newCommunity.html", {})


# TODO: BURANIN ALTI FENA----- BUNLARI TEK TEK ELDEN GEÇİR
@csrf_exempt
def tags(request):
    query = request.POST.get("query", "")
    data = WikidataService.query(query)
    return JsonResponse(data, safe=False)


# TODO: ÇALIŞMIYOR
def searchTag_view(request):
    txtSRC = request.GET.get('search_text')
    SEARCHPAGE = txtSRC
    PARAMS = {
        "action": "query",
        "format": "json",
        "list": "search",
        "srsearch": SEARCHPAGE
    }
    Srch = requests.Session()
    URL = "https://en.wikipedia.org/w/api.php"
    Res = Srch.get(url=URL, params=PARAMS)
    DATA = Res.json()['query']['search']
    titles = ""
    for tt in DATA:
        titles += "#" + tt['title']
    return render(request, 'komunitipage/tagSearch.html', {'form': titles})


def CreateCommunity_view(request):
    form = AddCommunity(request.POST, request.FILES)
    comm = Community
    comm.title = request.POST.get("Community_Name")
    comm.description = request.POST.get("Community_Description")

    community_tag = CommunityTag()
    comm.communityTags = request.POST.get("Community_Tags")

    return render(request, 'komunitipage/CreateCommunity.html', {'form': form}, )
