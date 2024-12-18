import json
from channels.generic.websocket import AsyncWebsocketConsumer
from django.utils.timezone import now
from .models import ChatRoom, Message
from django.contrib.auth import get_user_model

User = get_user_model()

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.chatroom_id = self.scope['url_route']['kwargs']['chatroom_id']
        self.room_group_name = f'chat_{self.chatroom_id}'

        # Add the WebSocket connection to the room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Remove the WebSocket connection from the room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        data = json.loads(text_data)
        message_content = data['message']
        username = self.scope['user'].username

        # Save the message to the database
        user = await self.get_user(self.scope['user'].id)
        chatroom = await self.get_chatroom(self.chatroom_id)
        message = await self.save_message(chatroom, user, message_content)

        # Broadcast the message to the group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message.content,
                'username': username,
                'timestamp': message.timestamp.strftime("%H:%M"),
            }
        )

    async def chat_message(self, event):
        # Send the message to WebSocket
        await self.send(text_data=json.dumps({
            'message': event['message'],
            'username': event['username'],
            'timestamp': event['timestamp'],
        }))

    @staticmethod
    async def get_user(user_id):
        return await User.objects.aget(id=user_id)

    @staticmethod
    async def get_chatroom(chatroom_id):
        return await ChatRoom.objects.aget(id=chatroom_id)

    @staticmethod
    async def save_message(chatroom, user, content):
        return await Message.objects.acreate(
            chatroom=chatroom,
            sender=user,
            content=content,
            timestamp=now()
        )
