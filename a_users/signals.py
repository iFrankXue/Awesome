from django.dispatch import receiver
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404

from allauth.account.models import EmailAddress
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


@receiver(post_save, sender=Profile)
def update_account_email(sender, instance, created, **kwargs):
    profile = instance
    if not created:
        try: 
            email_address = EmailAddress.objects.get_primary(profile.user)
            if email_address.email != profile.email:
                email_address.email = profile.email
                email_address.verified = False
                email_address.save()
        except:
            pass