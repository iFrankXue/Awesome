from django.urls import path
from .views import *

urlpatterns = [
    path('', inbox_view, name='inbox'),
    path('c/<str:conversation_id>/', inbox_view, name='inbox'),
    path('search_users/', search_users, name='inbox-searchusers'),
    path('new_message/<str:recipient_id>', new_message, name='inbox-newmessage'),
    path('new_reply/<str:conversation_id>/', new_reply, name='inbox-newreply'),

    path('notify/inbox', notify_inbox, name='notify-inbox'),
    path('notify/<str:conversation_id>/', notify_newmessage, name='notify-newmessage'),
]
