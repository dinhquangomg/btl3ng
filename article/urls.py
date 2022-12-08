from django.urls import path
from .views import home, PostList


urlpatterns = [
    path('', home , name='home' )
    # path('', PostList.as_view(), name='home'),
]
