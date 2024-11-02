# chatapp/consumers/chat_consumer.py
from channels.generic.websocket import AsyncWebsocketConsumer
import json 
from asgiref.sync import sync_to_async
from ..models import PublicChatRoom, Message
from django.contrib.auth.models import User
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
import base64
class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_slug = f"room_{self.scope['url_route']['kwargs']['room_slug']}"
        self.room_group_name = 'chat_%s' % self.room_slug

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

        self.send(text_data=json.dumps({
            'type':'connection established',
            'message': 'you are now connected'
        }))

    async def disconnect(self,code ):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )
        self.close(code)

    async def receive(self, text_data):
        # Process received a message
        data_json = json.loads(text_data)
        username = data_json['username']
        message = data_json['message']
        room_slug = data_json['room_slug']
        profile_pic = data_json['profile_pic']
        timestamp = data_json['timestamp']
        file_name = data_json['file_name']
        file_data = data_json['file_data']
        
        # decoded_data = base64.b64decode(file_data.split(',')[1])
        # data = ("files/"+file_name, ContentFile(decoded_data))
        data = None
        if (file_data !=  None):
            try:
                format, imgstr = file_data.split(';base64,')
                data = ContentFile(base64.b64decode(imgstr), name= file_name) # You can save this as file instance.
            except:
                pass
        await self.save_message(username, message, room_slug,data)

        
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type':'send_message',
                'username':username,
                'message':message,
                'room_slug':room_slug,
                'profile_pic':profile_pic,
                'timestamp':timestamp,
                'file_data': file_data
            }
        )

    async def send_message(self, event):
        # Send a message to WebSocket
        username = event['username']
        message = event['message']
        room_slug = event['room_slug']
        profile_pic = event['profile_pic']
        timestamp = event['timestamp']
        file_data = event['file_data']
        await self.send(text_data=json.dumps({
            'username':username,
            'message':message,
            'room_slug':room_slug,
            'profile_pic':profile_pic,
            'timestamp':timestamp,
            'file_data': file_data
        }))
    
    @sync_to_async
    def save_message(self, username, message, room_slug,file):
        room = PublicChatRoom.objects.get(slug=room_slug)
        sender = User.objects.get(username=username)
        Message.objects.create(room=room, sender=sender, content=message,file=file)
