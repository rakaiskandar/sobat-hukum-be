from rest_framework import serializers
from .models import Conversations, Messages

class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Messages
        fields = ['message_id', 'user_id', 'message_content', 'sent_at', 'is_read']

class ConversationSerializer(serializers.ModelSerializer):
    messages = MessageSerializer(many=True, read_only=True)

    class Meta:
        model = Conversations
        fields = ['conversation_id', 'case_id', 'client_id', 'lawyer_id', 'created_at', 'messages']