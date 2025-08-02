from rest_framework.permissions import BasePermission, IsAuthenticated
from rest_framework import permissions

class IsOwner(BasePermission):
    """
    Custom permission to allow users to access only their own objects.
    """

    def has_object_permission(self, request, view, obj):
        return obj.user == request.user  # Adjust if needed
    def has_permission(self, request, view):
        # Allow access only if the user is authenticated
        return request.user and request.user.is_authenticated