from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from .models import *


def home(request):
    community = get_object_or_404(Community,title='Com1')
    return render(request, 'komunitipage/home.html', {'com':community})
def hello(request):
    return HttpResponse("Hello Wordl")