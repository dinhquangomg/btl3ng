from django.shortcuts import render
from django.views.generic import ListView
from .models import Post

# Create your views here.
def home(request):
    section = "home"
    posts = Post.objects.all()
    return render(
        request=request,
        template_name='article/home.html',
        context= {'section':section, 'posts':posts}
    )

class PostList(ListView):
    model = Post
    template_name = 'article/home.html'
