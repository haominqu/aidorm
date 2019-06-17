from rest_framework import permissions
from rest_framework_jwt.utils import jwt_decode_handler

#
# MROLE_CHIOCES = (
#     (0, "超级管理员"),
#     (1, "学校管理员"),
#     (2, "基础设施管理"),
#     (3, "导员"),
#     (4, "宿舍管理员"),
# )


class IsSchoolAdmin(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    """

    def has_permission(self, request, view):

        token = request.META.get("HTTP_AUTHORIZATION", "")
        if token == "":
            return False
        token = token.split(' ')
        a = jwt_decode_handler(token[2])
        if request.method == 'GET':
            if a['role'] == 1 or a['role'] == 3 or a['role'] == 4:
                return True
            else:
                return False
        else:
            if a['role'] == 1:
                return True
            else:
                return False

        # Read permissions are allowed to any request
        # if request.method == 'GET':
        #     token = request.META.get("HTTP_AUTHORIZATION").split(' ')
        #     a = jwt_decode_handler(token[2])
        #     if a['role'] == 1:
        #         return True
        #     else:
        #         return False
        # return False

