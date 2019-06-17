from rest_framework import permissions
from rest_framework_jwt.utils import jwt_decode_handler


class IsSuperAdmin(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    """

    def has_permission(self, request, view):

        # Read permissions are allowed to any request
        token = request.META.get("HTTP_AUTHORIZATION").split(' ')
        a = jwt_decode_handler(token[2])
        if a['role'] == 0:
                return True
        else:
            return False
