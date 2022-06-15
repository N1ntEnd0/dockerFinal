from django.http import HttpResponseForbidden
from django.utils.deprecation import MiddlewareMixin
from rest_framework_simplejwt.exceptions import AuthenticationFailed
from social_django.models import UserSocialAuth

from users.utils import check_tokens, refresh_user_social_tokens


class CheckSocialAuthToken:

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):

        response = self.get_response(request)

        user = request.user
        try:
            check_tokens(user, provider='google-oauth2')
        except UserSocialAuth.DoesNotExist:
            pass
        except AuthenticationFailed:
            refresh_user_social_tokens(user, provider='google-oauth2')
        return response





