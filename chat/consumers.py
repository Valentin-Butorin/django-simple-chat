import json
from datetime import datetime

from channels.generic.websocket import AsyncWebsocketConsumer


class ChatConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        self.group_name = 'chat'
        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, code):
        await self.channel_layer.group_discard(self.group_name, self.channel_name)

    async def receive(self, text_data=None, bytes_data=None):
        data_json = json.loads(text_data)
        message = data_json['message']
        username = data_json['username']

        if not username:
            username = 'Anonymous'

        dt = datetime.now().strftime('%d.%m.%Y %H:%M')

        result = f'{dt} - {username} - {message}'

        event = {
            'type': 'send_message',
            'message': result
        }

        await self.channel_layer.group_send(self.group_name, event)

    async def send_message(self, event):
        message = event['message']

        await self.send(text_data=json.dumps({'message': message}))
