from django.shortcuts import render, redirect
from django.views.generic import ListView
from .models import Post, Tag
from django.contrib.auth.decorators import login_required
from .forms import PostCreateForm
from django.http import HttpResponse
from django.http import JsonResponse
from django.contrib.auth.models import User
from random import sample
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.urls import reverse, reverse_lazy


@login_required
def ajax_like(requset):
    post_id = requset.GET.get('post_id')
    user = requset.user
    post = Post.objects.get(id=post_id)
    users_like = post.likes.all()
    if user in users_like:
        post.likes.remove(user)
    else:
        post.likes.add(user)
    users_like = post.likes.all()
    number_like = len(list(users_like))
    return JsonResponse({'number_like':number_like}, status=200)
    

@login_required
def ajax_bookmark(requset):
    posts = requset.user.profile.bookmark.all()
    post_id = requset.GET.get('post_id')
    user = requset.user
    post = Post.objects.get(id=post_id)
    if post in posts:
        user.profile.bookmark.remove(post)
    else:
        user.profile.bookmark.add(post)
    return JsonResponse({'message':'success'}, status=200)

def demo(request):
    print('haha')
    if request.method=='GET':
        i = request.GET['text']


        return JsonResponse({'text':'quangdeptrai'}, status=200)

def personal_page(requset):
    pass


@login_required
def delete_bookmark(request, post_id):
    user = request.user
    post = Post.objects.get(id=post_id)
    user.profile.bookmark.remove(post)
    return redirect('article:bookmark')

@login_required
def add_bookmark(request, post_id):
    user = request.user
    post = Post.objects.get(id=post_id)
    user.profile.bookmark.add(post)
    return redirect('article:home')


@login_required
def bookmarks(request):
    posts = request.user.profile.bookmark.all()
    context = {'posts':posts}
    return render(
        request=request,
        template_name='article/bookmark.html',
        context=context
    )


@login_required
def tag(request):
    context = {'section':'tags'}
    user = request.user
    tags = user.profile.tags.all()
    new_tags = Tag.objects.all()
    context['tags'] = tags
    context['new_tags'] = new_tags
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
    posts_bookmark = request.user.profile.bookmark.all()
    users_like = post.likes.all()
    user = request.user
    bookmark = True if post in posts_bookmark else False
    like = True if user in users_like else False
    tag = post.tag
    number_like = len(list(users_like))
    more_posts = Post.objects.filter(tag=tag).exclude(id=post.id)
    context = {
        'post':post,
        'more_posts':more_posts,
        'bookmark': bookmark,
        'like': like,
        'number_like':number_like,
    }
    return render(request, 'article/detail.html', context=context)

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

    tags = Tag.objects.all()
    random_tags = sample(list(tags), 10)
    users = User.objects.all()
    posts = []
    context = {
            'random_tags':random_tags,
            'users':users,
        }

    page = request.GET.get('page', 1) 
    if str(request.user) == 'AnonymousUser':
        posts = Post.objects.all()
        paginator = Paginator(posts, 3)
    else:
        tags = request.user.profile.tags.all()
        for tag in tags:
            temp = Post.objects.filter(tag=tag)
            posts.extend(temp)

        if not len(posts):
            posts = Post.objects.all()
        
        paginator = Paginator(posts, 3)

        tags = request.user.profile.tags.all()
        context['tags'] = tags
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        page = 1
        posts = paginator.page(page)
    except EmptyPage:
        page = paginator.num_pages
        posts = paginator.page(page)

    print(page)

    context['posts'] = posts
    context['page'] = page
    print(page)
    

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
