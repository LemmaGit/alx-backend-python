from rest_framework import viewsets, permissions, status, filters
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.status import HTTP_403_FORBIDDEN  
from .models import Conversation, Message
from .serializers import ConversationSerializer, MessageSerializer
from .permissions import IsParticipantOfConversation  

class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated, IsParticipantOfConversation]

    def get_queryset(self):
        return Message.objects.filter(conversation__participants=self.request.user)

    def perform_create(self, serializer):
        conversation_id = self.request.data.get('conversation')
        try:
            conversation = Conversation.objects.get(id=conversation_id)
        except Conversation.DoesNotExist:
            return Response({"detail": "Conversation not found."}, status=status.HTTP_404_NOT_FOUND)

        if self.request.user not in conversation.participants.all():
            return Response({"detail": "Forbidden"}, status=HTTP_403_FORBIDDEN)

        serializer.save(user=self.request.user, conversation=conversation)
