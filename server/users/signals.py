from django.db.models.signals import post_save
from django.dispatch import receiver
from social_django.models import UserSocialAuth

from gdrive.utils import create_permissions


# @receiver(sender=UserSocialAuth, signal=post_save)
# def add_user_to_group(sender, instance, created, **kwargs):
#     if created:
#         print('create_permissions')
#         create_permissions(instance.user.username)
