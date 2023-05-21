from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver

from .models import Profile


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
        profile = Profile(user=instance)
        profile.save()
        print("Object created")
    else:
        try:
            Profile.objects.get(user=instance)
            print("hi 1")
        except:
            Profile.objects.create(user=instance)
            profile = Profile(user=instance)
            profile.save()
            print("hi2")
