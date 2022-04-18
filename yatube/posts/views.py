from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404, redirect
from .models import Post, Group, User, Follow
from .forms import PostForm, CommentForm
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect


def index(request):
    '''Главная страница'''
    search_query = request.GET.get('search', '')
    if search_query:
        posts = Post.objects.filter(text__icontains=search_query)
    else:
        posts = Post.objects.all()
    template = 'posts/index.html'
    title = 'Это главная страница проекта Yatube'
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'title': title,
        'page_obj': page_obj,
    }
    return render(request, template, context)


def group_posts(request, slug):
    '''Страница с постами отфильтрованная по группам'''
    template = 'posts/group_list.html'
    group = get_object_or_404(Group, slug=slug)
    posts = group.posts.all()
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'group': group,
        'page_obj': page_obj,
    }
    return render(request, template, context)


def profile(request, username):
    '''Профайл автора'''
    template = 'posts/profile.html'
    user_name = get_object_or_404(User, username=username)
    title = (f'Профайл пользователя: {user_name}')
    posts = Post.objects.filter(author=user_name)
    posts_count = posts.count()
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    user = request.user
    following = user.is_authenticated and user_name.following.exists()
    context = {
        'title': title,
        'user_name': user_name,
        'posts_count': posts_count,
        'page_obj': page_obj,
        'following': following
    }
    return render(request, template, context)


def post_detail(request, post_id):
    '''Информация о посте'''
    template = 'posts/post_detail.html'
    post = get_object_or_404(Post, pk=post_id)
    count = post.author.posts.count()
    form = CommentForm()
    comments = post.comments.all()
    context = {
        'post': post,
        'count': count,
        'form': form,
        'comments': comments
    }
    return render(request, template, context)


@login_required  # Доступно авторизированым пользователям
def post_create(request):
    '''Создать пост'''
    template = 'posts/create_post.html'
    title = 'Добавить запись'

    form = PostForm(request.POST or None)
    if form.is_valid():
        post = form.save(commit=False)
        post.author = request.user
        form.save()
        return redirect('posts:profile', post.author.username)

    context = {
        'title': title,
        'form': form
    }
    return render(request, template, context)


@login_required  # Доступно авторизированым пользователям
def post_edit(request, post_id):
    '''Изменить пост'''
    template = 'posts/create_post.html'
    is_edit = True
    title = 'Редактировать запись'
    post = get_object_or_404(Post, pk=post_id)

    form = PostForm(request.POST or None,
                    files=request.FILES or None,
                    instance=post
                    )
    if request.user == post.author and form.is_valid():
        form.save()
        return redirect('posts:post_detail', post.id)

    context = {
        'form': form,
        'is_edit': is_edit,
        'title': title
    }
    return render(request, template, context)


@login_required  # Доступно авторизированым пользователям
def post_delete(request, post_id):
    '''Удалить пост'''
    post = get_object_or_404(Post, pk=post_id)
    if request.user == post.author:
        post.delete()
    return redirect('posts:profile', post.author.username)


@login_required  # Доступно авторизированым пользователям
def add_comment(request, post_id):
    '''Добавить коментарий к посту'''
    # Получите пост
    post = get_object_or_404(Post, pk=post_id)
    form = CommentForm(request.POST or None)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.author = request.user
        comment.post = post
        comment.save()
    return redirect('posts:post_detail', post_id=post_id)


@login_required
def follow_index(request):
    template = 'posts/follow.html'
    user = request.user
    authors = user.follower.values_list('author', flat=True)
    posts = Post.objects.filter(author__id__in=authors)
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'template': template,
        'page_obj': page_obj
    }
    return render(request, template, context)


@login_required
def profile_follow(request, username):
    '''Подписаться на автора'''
    author = User.objects.get(username=username)
    user = request.user
    if author != user:
        Follow.objects.get_or_create(user=user, author=author)
        return redirect('posts:profile', username=username)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required
def profile_unfollow(request, username):
    '''Отписаться на автора'''
    user = request.user
    Follow.objects.get(user=user, author__username=username).delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
