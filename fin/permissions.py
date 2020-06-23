from rest_framework import permissions
from rest_framework.exceptions import PermissionDenied

class IsAutentificated(permissions.BasePermission):
    def has_permission(self, request, view):
        is_auth = bool(request.user and request.user.is_authenticated)
        if is_auth:
            return is_auth
        else:
            raise PermissionDenied(detail="User isn't autentificate!")