from rest_framework.permissions import BasePermission


class IsAnonymous(BasePermission):
    """
    Allows access only to anonymous users.
    """

    def has_permission(self, request, view):
        return request.user and not request.user.is_authenticated


class IsOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj == request.user
