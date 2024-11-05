"""
URL configuration for a_core project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView
from django.conf.urls.static import static
from django.conf import settings
from a_posts.views import *
from a_users.views import *

# from a_posts.views import *

urlpatterns = [
    # path('admin/', admin.site.urls),
    path('admin/', include('admin_honeypot.urls', namespace='admin_honeypot')),
    path('theboss/', admin.site.urls),
    
    
    path('accounts/', include('allauth.urls')),
    
    
    path('', home_view, name='home'),
    path('posts/create/', post_create_view, name='post-create'),
    path('posts/delete/<str:pk>', post_delete_view, name='post-delete'),
    path('posts/edit/<str:pk>/', post_edit_view, name='post-edit'),
    path('posts/show/<str:pk>/', post_page_view, name='post-page'),
    path('posts/like/<str:pk>/', post_like, name='post-like'),

    path('category/<str:slug>/', home_view, name='category-view'),

    path('comment/sent/<str:pk>/', comment_sent, name='comment-sent'),
    path('comment/delete/<str:pk>/', comment_delete, name='comment-delete'),
    path('comment/like/<str:pk>/', comment_like, name='comment-like'),

    path('reply/sent/<str:pk>/', reply_sent, name='reply-sent'),
    path('reply/delete/<str:pk>/', reply_delete, name='reply-delete'),
    path('reply/like/<str:pk>/', reply_like, name='reply-like'),
    
    path('profile/', profile_view, name='profile-view'),
    path('profile/edit/', profile_edit_view, name='profile-edit'),
    path('profile/delete/', profile_delete_view, name='profile-delete'),
    path('profile/view/<str:username>/', profile_view, name='user-profile'),
    path('profile/onboarding/', profile_edit_view, name='profile-onboarding'),
    path('profile/verify-email/', profile_verify_email, name='profile-verify-email'),
    
    
    path('inbox/', include('a_inbox.urls')),
    
]

# # Only for development
# urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
