from rest_framework import permissions


class IsSuperuser(permissions.BasePermission):
    """
    只有超级用户才能访问
    """

    def has_permission(self, request, view):
        return request.user and request.user.is_superuser
