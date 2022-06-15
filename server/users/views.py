from django.conf import settings
from django.db import transaction
from django.http import JsonResponse
from django.shortcuts import render
# Create your views here.
from django.views import View
from djoser.social.views import ProviderAuthView

from gdrive.utils import create_permissions


class RedirectSocial(View):

    def get(self, request, *args, **kwargs):
        code, state = str(request.GET.get('code')), str(request.GET.get('state'))
        json_obj = {'code': code, 'state': state}
        return JsonResponse(json_obj)




class CustomProviderAuth(ProviderAuthView):

    @transaction.atomic
    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        username = response.data.get('user')
        # create_permissions(username)
        return response
