from django.contrib import admin
from django.urls import path
from komunitipage import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('hello', views.hello, name='hello')


]
