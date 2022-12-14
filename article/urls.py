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
    path('unfollow_tag/<str:tag>/', views.unfollow_tag, name='unfollow_tag')
]
