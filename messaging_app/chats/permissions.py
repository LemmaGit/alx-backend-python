from rest_framework.permissions import BasePermission

class IsOwner(BasePermission):
    """
    Custom permission to allow users to access only their own objects.
    """

    def has_object_permission(self, request, view, obj):
        # Adjust 'user' to your model's field, e.g., obj.owner or obj.sender
        return obj.user == request.user
