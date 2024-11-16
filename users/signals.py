from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import Profile
from friends.models import Friendlist
@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    """ the objectif of this method is to create a profile for a user after he is created
        once the user is created it's received by the receiver
        instance contains the information of the user
    """
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
    """ the objectif of this method is to save the profile every time a user gets saved
    """
    instance.profile.save()