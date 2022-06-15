import time

from django.conf import settings
from django.contrib.auth import password_validation, get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from rest_framework_simplejwt.exceptions import AuthenticationFailed
from social_django.models import UserSocialAuth
from social_django.utils import load_strategy


def validate_credentials(username, email, password):
    if username is None:
        raise AttributeError('Username shouldn\'t be None')
    if email is None:
        raise AttributeError('Email shouldn\'t be None')
    if password is None:
        raise AttributeError('Password shouldn\'t be None')
    password_validation.validate_password(password)


def get_user_info(access_token):
    scopes = ['openid', 'https://www.googleapis.com/auth/userinfo.email',
              'https://www.googleapis.com/auth/userinfo.profile']
    credentials = Credentials(token=access_token, scopes=scopes)
    user_info_service = build('oauth2', 'v2', credentials=credentials)
    user_info = user_info_service.userinfo().get().execute()
    print(user_info['email'])
    print(user_info)
    return user_info

# def save_user(user_info):
#      User.objects.create(username='')



def check_tokens(user, provider):
    if user.is_anonymous:
        raise UserSocialAuth.DoesNotExist()
    print(user)
    social = user.social_auth.get(provider=provider)
    auth_time = social.extra_data['auth_time']
    expires = social.extra_data['expires']
    if check_token_exp(auth_time, expires):
        raise AuthenticationFailed()
    return social



def get_main_user_token(user):
    social = check_and_refresh_token(user, 'google-oauth2')
    return social.extra_data['access_token']



def check_token_exp(auth_time, expires):
    if auth_time + expires <= int(time.time()):
        return True
    return False

def check_and_refresh_token(user, provider):
    try:
        social = check_tokens(user, provider)
    except AuthenticationFailed:
        print('refresh')
        social = refresh_user_social_tokens(user, provider)
    return social

def refresh_user_social_tokens(user, provider):
    social = user.social_auth.get(provider=provider)
    strategy = load_strategy()
    social.refresh_token(strategy)
    return social


def get_host_by_request(request):
    print(request.META.get('HTTP_HOST'))
    return True


@receiver(post_save, sender=settings.AUTH_USER_MODEL, dispatch_uid='post_save_user')
def post_save_user(sender, instance, created, **kwargs):
   pass













