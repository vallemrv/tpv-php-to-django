# @Author: Manuel Rodriguez <valle>
# @Date:   10-Jun-2018
# @Email:  valle.mrv@gmail.com
# @Last modified by:   valle
# @Last modified time: 19-Jun-2018
# @License: Apache license vesion 2.0


# chat/consumers.py
from asgiref.sync import async_to_sync
from channels.generic.websocket import AsyncWebsocketConsumer
import json


class ImpresionConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.print_name = self.scope['url_route']['kwargs']['print_name']
        self.print_group_name = 'print_%s' % self.print_name

        # Join room group
        await self.channel_layer.group_add(
            self.print_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.print_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        # Send message to room group
        await self.channel_layer.group_send(
            self.print_group_name,
            {
                'type': 'print_message',
                'message': message
            }
        )

    # Receive message from room group
    async def print_message(self, event):
        message = event['message']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message
        }))
