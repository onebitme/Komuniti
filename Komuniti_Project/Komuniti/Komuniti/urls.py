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
    path('communities', views.communities, name='communities'),
    path('hello', views.hello, name='hello'),
    path('community_edit', views.post_new, name='post_add'),
    path('community_search', views.community_search, name='community_search'),
    path('add_datatype', views.add_datatype, name='komunitipage/add_datatype')
    ##path('search/', views.SearchResultsView, name='search_results'),
    ##path('seach_results',views.seach, name='search')
]
