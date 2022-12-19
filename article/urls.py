from django.urls import path
from .views import home, PostList, post_create, home_with_tag, detail, add_tag
from . import views

app_name = 'article'

urlpatterns = [
    path('', home , name='home' ),
    path('create/', post_create, name='create'),
    path('tag/<str:tag>/', home_with_tag, name = 'home_with_tag'),
    path('post/<int:id>/', detail, name='post_detail'),
    path('addtag/', add_tag, name='add_tag'),
    path('tags/', views.tag, name='tag_manager'),
    path('unfollow_tag/<str:tag>/', views.unfollow_tag, name='unfollow_tag'),
    path('bookmarks/', views.bookmarks, name='bookmark'),
    path('add_bookmark/<int:post_id>/', views.add_bookmark, name='add_bookmark'),
    path('delete_bookmark/<int:post_id>/', views.delete_bookmark, name='delete_bookmark'),
    path('demo/', views.demo, name='demo'),
    path('ajax_bookmark/', views.ajax_bookmark, name='ajax_bookmark'),


]
