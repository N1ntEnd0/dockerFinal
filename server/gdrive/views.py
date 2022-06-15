from collections import OrderedDict
from typing import List, Any

from django.conf import settings

# Create your views here.
from django.contrib.auth import get_user_model
from django.core.paginator import Paginator
from django.http import JsonResponse
from rest_framework import viewsets
from rest_framework.decorators import action, api_view
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response

from gdrive import utils
from gdrive.models import GDFile
from gdrive.serializers import GDFileSerializer
from gdrive.utils import create_permissions
from users.utils import check_and_refresh_token


class ListPaginator:

    def __init__(self, request: Request):
        # Hidden HtmlRequest properties/methods found in Request.
        self._url_scheme = request.scheme
        self._host = request.get_host()
        self._path_info = request.path_info

    def paginate_list(self, data: List[Any], page_number, page_size):
        paginator = Paginator(data, page_size)
        page = paginator.page(page_number)

        previous_url = None
        next_url = None
        if self._host and self._path_info:
            if page.has_previous():
                previous_url = '{}://{}{}?page={}&page_size={}'.format(self._url_scheme, self._host, self._path_info,
                                                                       page.previous_page_number(), page_size)
            if page.has_next():
                next_url = '{}://{}{}?page={}&page_size={}'.format(self._url_scheme, self._host, self._path_info,
                                                                   page.next_page_number(), page_size)

        response_dict = OrderedDict([
            ('count', len(data)),
            ('next', next_url),
            ('previous', previous_url),
            ('results', page.object_list)
        ])
        return response_dict


class GDriveViewSet(viewsets.GenericViewSet):
    permission_classes = [IsAuthenticated, ]
    lookup_field = 'id'
    serializer_class = GDFileSerializer

    @action(detail=True, methods=['POST'])
    def download(self, request, *args, **kwargs):
        download_url = utils.download_file(request.user, settings.SOCIAL_AUTH_DEFAULT_PROVIDER,
                                           settings.SOCIAL_AUTH_GOOGLE_OAUTH2_SCOPE, file_id=self.kwargs.get('id'))
        return JsonResponse({'download_url': download_url})

    @action(detail=False, methods=['GET'])
    def get_from_google(self, request, *args, **kwargs):
        files = utils.get_user_files(provider=settings.SOCIAL_AUTH_DEFAULT_PROVIDER,
                                     scopes=settings.SOCIAL_AUTH_GOOGLE_OAUTH2_SCOPE)
        return Response(self.paginate_queryset(files))

    def paginate_queryset(self, queryset):
        page_number, page_size = self.request.query_params.get('page'), self.request.query_params.get('page_size')
        if page_number is None or page_size is None:
            return queryset

        paginator = ListPaginator(self.request)
        return paginator.paginate_list(queryset, page_number, page_size)


@api_view(["GET"])
def health(request):
    if request.method == 'GET':
        return Response({"detail": "ok"})