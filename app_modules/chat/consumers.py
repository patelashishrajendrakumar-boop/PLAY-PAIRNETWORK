import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from .models import Message

class ChatConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f'chat_{self.room_name}'
        print(f"Connecting to room: {self.room_name}")

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()
        print(f"Accepted connection for room: {self.room_name}")

    async def disconnect(self, close_code):
        print(f"Disconnecting from room: {self.room_name} with code {close_code}")
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        print(f"Received data: {text_data}")
        data = json.loads(text_data)
        message = data['message']
        username = self.scope["user"].username
        print(f"Message from {username}: {message}")

        # Save message to database
        await self.save_message(username, self.room_name, message)

        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'username': username
            }
        )

    async def chat_message(self, event):
        message = event['message']
        username = event['username']
        print(f"Broadcasting message from {username}")

        
        await self.send(text_data=json.dumps({
            'message': message,
            'username': username
        }))

    @database_sync_to_async
    def save_message(self, username, room_name, message):
        print(f"Saving message to DB: {message}")
        from django.contrib.auth import get_user_model
        User = get_user_model()
        user = User.objects.get(username=username)
        msg = Message.objects.create(sender=user, room_name=room_name, content=message)
        print(f"Saved message ID: {msg.id}")