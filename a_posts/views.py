from django.shortcuts import render, redirect, get_object_or_404, get_list_or_404
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.contrib import messages
from django.db.models import Count
from django.http import JsonResponse, HttpResponse

from bs4 import BeautifulSoup
import requests

from .models import Post, Tag, Comment, Reply
from .forms import PostCreateForm, PostEditForm, CommentCreateForm, ReplyCreateForm
from .utils import validate_uuid
# Create your views here.

def home_view(request, slug=None):
    if slug:
        posts = Post.objects.filter(tags__slug=slug)
        tag = get_object_or_404(Tag, slug=slug)
    else:
        posts = Post.objects.all()
        tag = None 
    
    paginator = Paginator(posts, 3)
    page = int(request.GET.get('page', 1))
    
    try:
        posts = paginator.page(page)
    except:
        return HttpResponse('')
    
    context = {
        'posts': posts,
        'page': page,
        'tag': tag,
    }
    
    if request.htmx:
        return render(request, 'snippets/loop_home_posts.html', context)
    else:
        return render(request, 'a_posts/home.html', context)


@login_required
def post_create_view(request):
    form = PostCreateForm()
    
    if request.method == 'POST':
        form = PostCreateForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)

            website = requests.get(form.data['url'])
            sourcecode = BeautifulSoup(website.text, 'html.parser')

            find_image = sourcecode.select('meta[content^="https://live.staticflickr.com"]')
            image = find_image[0]['content']
            post.image = image
            
            find_title = sourcecode.select('h1.photo-title')
            title = find_title[0].text.strip()
            post.title = title
            
            find_artist = sourcecode.select('a.owner-name')
            artist = find_artist[0].text.strip()
            post.artist = artist
            
            post.author = request.user
            
            post.save()
            form.save_m2m()
            return redirect('home')
    
    context = {
        'form': form
    }
    return render(request, 'a_posts/post_create.html', context)


@login_required
def post_delete_view(request,pk):
    validate_uuid(pk)
    post = get_object_or_404(Post, id=pk, author=request.user)
    
    if request.method == "POST":
        post.delete()
        messages.success(request, 'Post deleted successfully!')
        return redirect('home')
    
    context = {
        'post': post,
    }
    return render(request, 'a_posts/post_delete.html', context)


@login_required
def post_edit_view(request, pk):
    validate_uuid(pk)
    post = get_object_or_404(Post, id=pk, author=request.user)
    
    if request.method == "POST":
        form = PostEditForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            messages.success(request, 'Post edited successfully!')
            return redirect('home')
    else:
        form = PostEditForm(instance=post)
    
    context = {
        'post': post,
        'form': form,
    }
    return render(request, 'a_posts/post_edit.html', context)


def post_page_view(request, pk):
    validate_uuid(pk)    
    post = get_object_or_404(Post, id=pk)
    comment_form = CommentCreateForm()
    reply_form = ReplyCreateForm()
    
    if request.htmx:
        if 'top' in request.GET:
            comments = post.comments.annotate(like_count=Count('likes')).filter(like_count__gt=0).order_by('-like_count', '-created')
        else:
            comments = post.comments.all()
    
        context = {
            'comments': comments,
            'reply_form': reply_form,
        }
        return render(request, 'snippets/loop_postpage_comments.html', context)
    
    context = {
        'post': post,
        'comment_form': comment_form,
        'reply_form': reply_form,
    }    
    return render(request, 'a_posts/post_page.html', context)


@login_required
def comment_sent(request, pk):
    validate_uuid(pk)
    post = get_object_or_404(Post, id=pk)
    comment = None
    
    reply_form = ReplyCreateForm()
    
    if request.method == 'POST':
        form = CommentCreateForm(request.POST)

        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.parent_post = post
            comment.save()

    context = {
        'comment': comment,
        'post': post,
        'reply_form': reply_form,
    }
    
    return render(request, 'snippets/add_comment.html', context)


@login_required
def comment_delete(request, pk):
    validate_uuid(pk)
    comment = get_object_or_404(Comment, id=pk, author=request.user)
    parent_post_id = comment.parent_post.id
    
    if request.method == 'POST':
        comment.delete()
        messages.success(request, 'Message deleted successfully!')
        return redirect('post-page', parent_post_id)
    
    context = {
        'comment': comment,
    }
    return render(request, 'a_posts/comment_delete.html', context)


@login_required
def reply_sent(request, pk):
    validate_uuid(pk)
    comment = get_object_or_404(Comment, id=pk)
    reply_form = ReplyCreateForm()
    
    if request.method == 'POST':
        form = ReplyCreateForm(request.POST)

        if form.is_valid():
            reply = form.save(commit=False)
            reply.author = request.user
            reply.parent_comment = comment
            reply.save()

    context = {
        'reply': reply,
        'comment': comment,
        'reply_form': reply_form,
    }    
    return render(request, 'snippets/add_reply.html', context)


@login_required
def reply_delete(request, pk):
    validate_uuid(pk)
    reply = get_object_or_404(Reply, id=pk, author=request.user)
    parent_post_id = reply.parent_comment.parent_post.id
    
    if request.method == 'POST':
        reply.delete()
        messages.success(request, 'Reply deleted successfully!')
        return redirect('post-page', parent_post_id)
    
    context = {
        'reply': reply,
    }
    return render(request, 'a_posts/reply_delete.html', context)




def like_toggle(model): 
    def inner_func(func):
        def wrapper(request, *args, **kwargs):

            instance = get_object_or_404(model, id=kwargs.get('pk'))
            user_exist = instance.likes.filter(username=request.user.username).exists()
            
            if instance.author != request.user:
                if user_exist:
                    instance.likes.remove(request.user)
                else:
                    instance.likes.add(request.user)
            
            return func(request, instance)
        return wrapper
    return inner_func


@login_required
@like_toggle(Post)
def post_like(request, instance):
    context = {
        'post': instance,
    }   
    return render(request, 'snippets/post_likes.html', context)

@login_required
@like_toggle(Comment)
def comment_like(request, instance):
    context = {
        'comment': instance,
    }
    return render(request, 'snippets/comment_likes.html', context)

@login_required
@like_toggle(Reply)
def reply_like(request, instance):
    context = {
        'reply': instance,
    }
    return render(request, 'snippets/reply_likes.html', context)
