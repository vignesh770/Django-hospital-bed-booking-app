from channels.generic.websocket import AsyncWebsocketConsumer, AsyncJsonWebsocketConsumer
from django.db.models import Q
from asgiref.sync import sync_to_async

import json

from userapp.models import Account
from hospital.models import Hospital
from .models import Thread, Notification


class NotificationConsumer(AsyncJsonWebsocketConsumer):

    async def connect(self):

        reference_user = self.scope['user']     # logged in user

        # create a new Thread object if thread of specific chat does not exists, otherwise return the thread
        thread = None
        try:
            thread = await sync_to_async(Thread.objects.get, thread_sensitive=True)(Q(user=reference_user))
        except:
            thread = await sync_to_async(Thread.objects.create, thread_sensitive=True)(user=reference_user)

        self.room_name = thread.unique_room_id   # room name

        await self.channel_layer.group_add(
            self.room_name,
            self.channel_name
        )

        await self.accept()


    async def disconnect(self, close_code):
        '''
            disconnect the websocket connection.
        '''
        await self.channel_layer.group_discard (
            self.room_name,
            self.channel_name
        )


    async def send_notification(self, event):
        notification = event['notification']
        booking_request_id = event['id']
        data = {
            'notification': notification, 
            'id': booking_request_id
        }
        await self.send_json(data)


        
        

