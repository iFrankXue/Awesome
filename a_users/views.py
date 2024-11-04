from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import Http404
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import logout
from django.urls import reverse
from django.db.models import Count

from a_posts.models import Post
from a_posts.forms import ReplyCreateForm

from .forms import ProfileForm
from a_inbox.forms import InboxNewMessageForm

# Create your views here.
def profile_view(request, username=None):
    if username:
        profile = get_object_or_404(User, username=username).profile
    else:
        try: 
            profile = request.user.profile
        except:
            raise Http404

    # Get posts for the profile
    posts = profile.user.posts.all()

    # Handling HTMX-specific requests
    if request.htmx:
        if 'top_posts' in request.GET:
            posts = profile.user.posts.annotate(top_points=Count('likes')).filter(top_points__gt=0).order_by('-top_points')
        elif 'top_comments' in request.GET:
            comments = profile.user.comments.annotate(top_points=Count('likes')).filter(top_points__gt=0).order_by('-top_points')
            reply_form = ReplyCreateForm()
            return render(request, 'snippets/loop_profile_comments.html', {'comments': comments, 'reply_form': reply_form}) 
        elif 'liked_posts' in request.GET:
            posts = profile.user.likedposts.order_by('-likedpost__created')
        
        return render(request, 'snippets/loop_profile_posts.html', {'posts': posts,}) 

    new_message_form = InboxNewMessageForm()
    
    context = {
        'profile': profile,
        'posts': posts,
        'new_message_form': new_message_form
    }
    return render(request, 'a_users/profile.html', context)


@login_required
def profile_edit_view(request):
    if request.method == "POST":
        form = ProfileForm(request.POST, request.FILES, instance=request.user.profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('profile-view')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = ProfileForm(instance=request.user.profile)  

    context = {
        'form': form    
    }

    if request.path == reverse('profile-onboarding'):
        template = 'onboarding'
    else:
        template = 'edit'
    template = 'a_users/profile_' + template + '.html'
    
    return render(request, template, context)


@login_required
def profile_delete_view(request):
    user = request.user
    
    if request.method == 'POST':
        logout(request)
        user.delete()
        messages.success(request, 'Account deleted, what a pity.')
        return redirect('home')
        
    return render(request, 'a_users/profile_delete.html')