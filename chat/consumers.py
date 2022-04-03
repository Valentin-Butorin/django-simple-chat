import json
from datetime import datetime
from channels.generic.websocket import AsyncWebsocketConsumer

CLIENTS = set()


class ChatConsumer(AsyncWebsocketConsumer):

    def get_secret_key(self):
        for key, value in self.scope['headers']:
            if key == b'sec-websocket-key':
                return value.decode(encoding='utf-8')
        return None

    async def connect(self):
        self.group_name = 'chat'
        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()

        key = self.get_secret_key()
        if key:
            CLIENTS.add(key)

            event = {
                'type': 'send_message',
                'users_count': len(CLIENTS)
            }

            await self.channel_layer.group_send(self.group_name, event)

    async def disconnect(self, code):
        key = self.get_secret_key()
        if key:
            CLIENTS.remove(key)

            event = {
                'type': 'send_message',
                'users_count': len(CLIENTS)
            }
            await self.channel_layer.group_send(self.group_name, event)

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
        response = dict()

        message = event.get('message')
        if message:
            response['message'] = message

        users_count = event.get('users_count')
        if users_count:
            response['users_count'] = users_count

        await self.send(text_data=json.dumps(response))
