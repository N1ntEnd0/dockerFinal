from rest_framework.permissions import BasePermission, SAFE_METHODS
from .utils import get_host_by_request

class IsHostOnly(BasePermission):

    # def has_permission(self, request, view):
    #     return True

    def has_object_permission(self, request, view, obj):

        return bool(request.method in SAFE_METHODS and get_host_by_request(request))
