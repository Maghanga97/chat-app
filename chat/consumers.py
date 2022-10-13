from channels.generic.websocket import AsyncWebsocketConsumer
import json
from asgiref.sync import sync_to_async
from .models import Room, Message
from chat.views import room

class ChatRoomConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room =self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room
        await self.channel_layer.group_add(
            self.room_group_name, 
            self.channel_name
        )

        await self.accept()

    async def disconnect(self):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        data = json.loads(text_data)
        message = data['message']
        room = data['room']

        await self.insert_message_to_db(message, room)
        
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'room': room
            }
        )

    async def chat_message(self, event):
        message = event['message']
        room = event['room']

        await self.send(text_data=json.dumps({
                'message': message,
                'room': room
        }))


    @sync_to_async
    def insert_message_to_db(self, message, room):
        chatroom = Room.objects.get(name=room)
        Message.objects.create(room=chatroom, text_msg=message)
