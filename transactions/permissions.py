from rest_framework import permissions


class IsOwner(permissions.BasePermission):
    """
    Custom permission that only allows the user to view and manipulate an
    object.
    """

    def has_object_permission(self, request, view, obj):
        return obj.user == request.user
