from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from .forms import PostForm
from .models import *


def home(request):
    return render(request, 'komunitipage/home.html') #,{'com':community})
def hello():
    return HttpResponse("Hello Bu Sadece bir HTTP Response")

def communities(request):

    if request.method == 'GET':  # If the form is submitted
        search_query = request.GET.get('search_post', None)

        if search_query != None:
            posts = Post.objects.filter(title__icontains=search_query)
        else:
            posts = None


    return render(request, 'komunitipage/communities.html', {'com': communities,'posts':posts})

def post_new(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        form.save()
    else:
        form = PostForm()
    return render(request, 'komunitipage/community_edit.html', {'post': form})


def post_search(request):
    #query = request.GET.get('search_post')
    template = 'komunitipage/home.html'
    #post = Post.objects.filter(title__icontains=query)


    if request.method == 'GET':  # If the form is submitted
        search_query = request.GET.get('search_post', None)

        if search_query != None:
            posts = Post.objects.filter(title__icontains=search_query)
        else:
            posts = Post.objects.all()


    return render(request,template, {'posts':posts})
