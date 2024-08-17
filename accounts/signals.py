from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from .models import User, UserProfile

@receiver(post_save, sender=User)
# post_save.connect(post_save_create_profile, sender=User)
def post_save_create_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)
        print("User profile is created !")

    else:
        try:
            profile = UserProfile.objects.get(user=instance)
            profile.save()
            print("User is updated !")    
        except:
            UserProfile.objects.create(user=instance)
            print("User profile is created !")   

@receiver(pre_save, sender=User)
def pre_save_create_user(sender, instance, **kwargs):
    # print(f"Creating {instance.username} in 3..2..1  Boom!")
    pass