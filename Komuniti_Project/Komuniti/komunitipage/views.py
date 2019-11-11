from django.db.models import Count
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from .forms import PostForm
from django.views.generic import ListView

from .models import *
import operator


def home(request):
    community = get_object_or_404(Community,title='Com1')
    return render(request, 'komunitipage/home.html', {'com':community})
def hello():
    return HttpResponse("Hello Bu Sadece bir HTTP Response")
def communities(request):
    return render(request, 'komunitipage/communities.html', {'com': communities})

def post_new(request):
    posts = PostForm()
    return render(request, 'komunitipage/community_edit.html', {'post': posts})

"""def search(request):
    if request.method == 'GET':  # If the form is submitted
        search_query = request.GET.get('search_community', None)

        if search_query != None:
            communities = Community.objects.filter(title__icontains=search_query).annotate(
                number_of_communities=Count('Community'))
        else:
            communities = Community.objects.annotate(number_of_communities=Count('Community'))
            communities = sorted(communities, key=operator.attrgetter('number_of_communities'), reverse=True)
        return 0;
        community = get_object_or_404(Community, title='Com2')
    return render(request,"komunitipage/search_results.html",{})"""