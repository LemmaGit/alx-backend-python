from rest_framework.permissions import BasePermission, IsAuthenticated, SAFE_METHODS
from rest_framework import permissions

class IsOwner(BasePermission):
    """
    Custom permission to allow users to access only their own objects.
    """

    def has_object_permission(self, request, view, obj):
        return obj.user == request.user  # Adjust if needed


class IsParticipantOfConversation(BasePermission):
    """
    Allow only participants of a conversation to view/edit messages.
    """

    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        # For read-only methods (GET, HEAD, OPTIONS)
        if request.method in SAFE_METHODS:
            return request.user in obj.conversation.participants.all()
        
        # For write methods (PUT, PATCH, DELETE)
        if request.method in ['PUT', 'PATCH', 'DELETE']:
            return request.user in obj.conversation.participants.all()

        return False