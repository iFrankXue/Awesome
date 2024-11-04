from django.dispatch import receiver
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404

from .models import Profile

@receiver(post_save,sender=User)
def create_profile(sender, instance, created, **kwargs):
    user = instance
    if created:
        Profile.objects.get_or_create(
            user=user, 
            defaults={'email': user.email}  # use defaults when using get_or_create function
        )
    else:
        profile = get_object_or_404(Profile, user=user)
        if profile.email != user.email:
            profile.email = user.email
            profile.save()
    
    
@receiver(post_save, sender=Profile)
def update_user(sender, instance, created, **kwargs):    
    if not created:
        profile = instance
        user = get_object_or_404(User, id=profile.user.id)
        if user.email != profile.email:
            user.email = profile.email
            user.save()
            