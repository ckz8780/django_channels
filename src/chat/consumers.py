import asyncio
import json
from django.contrib.auth import get_user_model
from channels.consumer import AsyncConsumer
from channels.db import database_sync_to_async

from .models import Thread, ChatMessage

class ChatConsumer(AsyncConsumer):
    async def websocket_connect(self, event):
        # When the socket connects
        print('Connected', event)
        await self.send({
            'type': 'websocket.accept'
        })

        other_user = self.scope['url_route']['kwargs']['username']
        me = self.scope['user']
        thread_obj = await self.get_thread(me, other_user)

    async def websocket_receive(self, event):
        # When a message is received from the websocket
        print('Received', event)
        front_text = event.get('text', None)
        if front_text is not None:
            loaded_dict_data = json.loads(front_text)
            msg = loaded_dict_data.get('message')
            print(msg)

        await self.send({
            'type': 'websocket.send',
            'text': msg
        })

    async def websocket_disconnect(self, event):
        # When the socket disconnects
        print('Disconnected', event)

    @database_sync_to_async
    def get_thread(self, user, other_username):
        return Thread.objects.get_or_new(user, other_username)[0]