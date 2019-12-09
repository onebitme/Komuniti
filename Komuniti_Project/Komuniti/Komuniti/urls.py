from django.contrib import admin
from django.urls import path,include
from rest_framework import routers
from django.conf.urls.static import static
from komunitipage import views


urlpatterns = [
    path('', views.home, name='home'),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('admin/', admin.site.urls),
    path('home', views.home, name='home'),
    path('community_' , views.communities, name='communities'),
    path('community_edit', views.post_new, name='post_add'),
    path('community_search', views.community_search, name='community_search'),
    path('upload_pic', views.upload_pic, name='komunitipage/upload_pic'),
    path('add_datatype',views.add_datatype, name='add_datatype'),
    path('show_datatype', views.show_datatype, name='show_datatype'),
    path('create_community',views.create_community, name='create_community'),
    path('test_2',views.show_datatype, name='komunitipage/test_2'),
    path('newCommunity',views.new_community, name='komunitipage/newCommunity'),
    #path('tagSearch',views.searchTag_view, name='komunitipage/tagSearch'),
    #path('CreateCommunity/', views.CreateCommunity_view, name="CreateCommunity"),

    #path('test', views.show_names, name='test'),
    ##path('search/', views.SearchResultsView, name='search_results'),
    ##path('seach_results',views.seach, name='search')
]
