from django.shortcuts import render, redirect
from django.views.generic import ListView
from .models import Post, Tag
from django.contrib.auth.decorators import login_required
from .forms import PostCreateForm


@login_required
def tag(request):
    context = {'section':'tags'}
    user = request.user
    tags = user.profile.tags.all()
    context['tags'] = tags
    return render(
        request=request,
        template_name='article/tags.html' ,
        context=context
    )
@login_required
def unfollow_tag(requset, tag):
    user = requset.user
    user.profile.tags.remove(Tag.objects.get(name=tag))
    return redirect('article:tag_manager')

def detail(request, id):
    post = Post.objects.get(pk=id)
    return render(request, 'article/detail.html', context={'post':post})

@login_required
def add_tag(request):
    if request.method == 'POST':
        tag_name = request.POST['tag']
        tag, get_bool = Tag.objects.get_or_create(name=tag_name)
        user = request.user
        user.profile.tags.add(tag)
    return redirect('article:home')
    
    

@login_required
def post_create(request):
    # if request.method == 'POST':
    #     # form is sent
    #     form = PostCreateForm(data=request.POST)
    #     if form.is_valid():
    #         # form data is valid
    #         new_item = form.save(commit=False)

    #         # assign current user to the item
    #         # new_item.user = request.user
    #         new_item.save()


    #         # redirect to new created item detail view
    #         return redirect('home')
    # else:
    #     form = PostCreateForm()
    if request.method == 'POST':
        # form is sent
        form = PostCreateForm(request.POST, request.FILES)
        if form.is_valid():
            # form data is valid
            # title = form.cleaned_data['title']
            tag_name = form.cleaned_data['tag']
            new_item = form.save(commit=False)

            tag, get_bool = Tag.objects.get_or_create(name=tag_name)
            new_item.author = request.user
            new_item.tag = tag
            new_item.save()
            # assign current user to the item
            # new_item.user = request.user


            # redirect to new created item detail view
            return redirect('article:home')
    else:
        form = PostCreateForm()
    # form = PostCreateForm()

    return render(request,
                  'article/create.html',
                  {'section': 'create',
                   'form': form})

# Create your views here.
def home(request):
    section = "home"
    tags = request.user.profile.tags.all()
    posts = []
    for tag in tags:
        temp = Post.objects.filter(tag=tag)
        posts.extend(temp)

    if not len(posts):
        posts = Post.objects.all()

    context= {'section':section, 'posts':posts, 'tag':None}
    if user := request.user:
        tags = user.profile.tags.all()
        context['tags'] = tags
    return render(
        request=request,
        template_name='article/home.html',
        context=context
    )

def home_with_tag(request, tag):
    section = "home"
    tag = Tag.objects.get(name=tag)
    posts = Post.objects.filter(tag=tag)
    context= {'section':section, 'posts':posts, 'tag':None}
    if user := request.user:
        tags = user.profile.tags.all()
        context['tags'] = tags
    return render(
        request=request,
        template_name='article/home.html',
        context=context
    )

class PostList(ListView):
    model = Post
    template_name = 'article/home.html'
