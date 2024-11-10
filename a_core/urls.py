from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView
from django.conf.urls.static import static
from django.views.generic.base import TemplateView

from django.conf import settings
from a_posts.views import *
from a_posts.sitemaps import *
from a_users.views import *


# Sitemaps
from django.contrib.sitemaps.views import sitemap

sitemaps = {
    'static': StaticSitemap,
    'categories': CategorySitemap,
    'postpages': PostpageSitemap,
}

urlpatterns = [
    path('sitemap.xml/', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
    path('robots.txt/', TemplateView.as_view(template_name='robots.txt', content_type='text/plain')),

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
    
    path('_/', include('a_landingpages.urls')),
    
]

# # Only for development
# urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
