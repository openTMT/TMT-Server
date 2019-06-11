from channels.generic.websocket import AsyncJsonWebsocketConsumer
import json


class ChatConsumer(AsyncJsonWebsocketConsumer):
    async def connect(self):
        self.room = None
        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        if self.room:
            await self.channel_layer.group_discard(self.room, self.channel_name)

    # Receive message from WebSocket
    async def receive_json(self, data):
        print(data)
        # data = {'room': '', 'to': '', 'message': '', }
        if data.get('message') == 'connect':
            self.room = data.get('room')
            await self.channel_layer.group_add(self.room, self.channel_name)
            return
        if self.room == None:
            return
        data['type'] = 'message'
        if data.get('to'):
            await self.channel_layer.group_send(data.get('to'), data)

    # Receive message from room group
    async def message(self, event):
        await self.send_json(event)
