from django import forms
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, render, redirect


from .models import Group, Post, User
from .forms import PostForm

"""
# создание поста под авторизацией.
@login_required
def post_create(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            text = form.cleaned_data['text']
            group = form.cleaned_data['group']
            form.save()
            return redirect('profile/<str:username>/')
        return render(request, 'posts/create_post.html', {'form': form})
    form = PostForm()
    return render(request, 'posts/create_post.html', {'form': form})


"""


@login_required
def post_create(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('posts:profile', request.user)
    else:
        form = PostForm()
    return render(
        request,
        'posts/create_post.html',
        {
            'form': form,
        },
    )


@login_required
def post_edit(request, post_id):
    is_edit = True
    post = get_object_or_404(Post, id=post_id)
    if post.author != request.user:
        return redirect('posts:post_detail', post_id)
    form = PostForm(request.POST, instance=post)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            return redirect('posts:post_detail', post_id)
    is_edit = True
    return render(
        request,
        'posts/create_post.html',
        {'post': post, 'form': form, 'is_edit': is_edit},
    )


# Главная страница
def index(request):
    posts = Post.objects.select_related('group', 'author')
    paginator = Paginator(posts, settings.NUMBER_OF_POSTS)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'posts/index.html', {'page_obj': page_obj})


# Страница групп
def group_posts(request, slug):
    group = get_object_or_404(Group, slug=slug)
    posts = group.posts.select_related('author')
    paginator = Paginator(posts, settings.NUMBER_OF_POSTS)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(
        request,
        'posts/group_list.html',
        {'group': group, 'page_obj': page_obj},
    )


# Профайл пользователя
def profile(request, username):
    author = get_object_or_404(User, username=username)
    posts = Post.objects.select_related('group', 'author').filter(
        author__username=username
    )
    paginator = Paginator(posts, settings.NUMBER_OF_POSTS)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    posts_count = posts.count()
    return render(
        request,
        'posts/profile.html',
        {
            'page_obj': page_obj,
            'author': author,
            'posts_count': posts_count,
        },
    )


# Отдельная запись
def post_detail(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    posts = Post.objects.filter(author__username=post.author.username)
    posts_count = posts.count()
    return render(
        request,
        'posts/post_detail.html',
        {
            'post': post,
            'posts_count': posts_count,
        },
    )
