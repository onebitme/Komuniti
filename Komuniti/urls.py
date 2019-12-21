from django.contrib import admin
from django.urls import path
from komunitipage import views
from Komuniti import settings
from django.contrib.staticfiles.urls import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

app_name = 'komunitipage'
urlpatterns = [
    path('', views.home, name='home'),
    path('advancedSearch', views.advancedSearch, name='advancedSearch'),
    path('admin/', admin.site.urls),
    path('home', views.home, name='home'),
    path('upload_pic', views.upload_pic, name='komunitipage/upload_pic'),
    path('create_community',views.create_community, name='create_community'),
    path('view_community/<int:communityId>',views.view_community, name='view_community'),
    path('add_post/<int:communityId>', views.add_post, name='add_post'),
    path('add2Community/<int:communityId>', views.add2Community, name='add2Community'),
    path('view_post/<int:postId>',views.view_post, name='view_post'),
    path('searchTag/<int:communityId>', views.searchTagCom, name='searchTag'),

    #Kommy Handlers!
    path('login', views.log_in, name='login'),
    path('logout', views.log_out, name='logout'),
    path('authenticated_user/', views.authenticated_user, name='authenticate_user'),
]

urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)