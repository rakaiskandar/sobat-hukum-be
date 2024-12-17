# consumers.py

import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from .models import Messages, Conversations
from .serializers import MessageSerializer

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.conversation_id = self.scope['url_route']['kwargs']['conversation_id']
        self.room_group_name = f"chat_{self.conversation_id}"

        # Join the chat group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        # Leave the chat group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        # Receive the message from WebSocket
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        # Save message to database
        await self.save_message(message)

        # Send message to WebSocket
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message
            }
        )

    async def chat_message(self, event):
        # Send the message to WebSocket
        message = event['message']
        await self.send(text_data=json.dumps({
            'message': message
        }))

    @database_sync_to_async
    def save_message(self, message):
        # Save message to database
        conversation = Conversations.objects.get(conversation_id=self.conversation_id)
        Messages.objects.create(
            conversation_id=conversation,
            user_id=self.scope['user'],
            message_content=message
        )
