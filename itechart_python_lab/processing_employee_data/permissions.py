from django.http import HttpResponseForbidden
from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsAdminOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return request.user
        return request.user.is_staff


def is_admin(func):
    def wrapper(*args, **kwargs):
        request = args[0]
        if request.user.is_staff:
            result = func(*args, **kwargs)
            return result
        return HttpResponseForbidden()
    return wrapper
