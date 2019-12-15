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
    path('view_community/<int:communityId>',views.view_community, name='view_community'),
    path('add_post/<int:communityId>', views.add_post, name='add_post'),
    path('add2Community/<int:communityId>', views.add2Community, name='add2Community'),
    path('view_post/<int:postId>',views.view_post, name='view_post')
]
