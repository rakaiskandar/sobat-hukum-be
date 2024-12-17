from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .models import Conversations, Messages
from .serializers import ConversationSerializer, MessageSerializer
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import status

class ConversationListView(generics.ListCreateAPIView):
    queryset = Conversations.objects.all()
    serializer_class = ConversationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Filter conversations based on the user (client or lawyer)
        user = self.request.user
        if user.role == 'client':
            return Conversations.objects.filter(client_id=user)
        elif user.role == 'lawyer':
            return Conversations.objects.filter(lawyer_id=user)
        return Conversations.objects.none()  # Return no conversations if no role

class MessageCreateView(generics.CreateAPIView):
    queryset = Messages.objects.all()
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user_id=self.request.user)

    @action(detail=True, methods=['get'])
    def get_messages(self, request, pk=None):
        conversation = self.get_object()
        messages = conversation.messages.all()
        serializer = MessageSerializer(messages, many=True)
        return Response(serializer.data)
