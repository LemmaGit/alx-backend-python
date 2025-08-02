from rest_framework.permissions import BasePermission, IsAuthenticated
from rest_framework import permissions

class IsOwner(BasePermission):
    """
    Custom permission to allow users to access only their own objects.
    """

    def has_object_permission(self, request, view, obj):
        return obj.user == request.user  # Adjust if needed


class IsParticipantOfConversation(BasePermission):
    """
    Allow access only to authenticated users who are participants
    of the conversation related to the message or conversation object.
    """

    def has_permission(self, request, view):
        # Allow only authenticated users
        return bool(request.user and request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        # Check if the user is a participant in the conversation
        # Adjust 'participants' or related field based on your models
        return request.user in obj.conversation.participants.all()