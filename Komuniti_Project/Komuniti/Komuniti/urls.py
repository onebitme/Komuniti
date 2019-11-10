from django.contrib import admin
from django.urls import path
from django.conf.urls.static import static
from komunitipage import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('communities', views.communities, name='communities'),
    path('hello', views.hello, name='hello'),
    path('community_edit', views.post_new, name='post_new')
    ##path('search/', views.SearchResultsView, name='search_results'),
    ##path('seach_results',views.seach, name='search')
]
