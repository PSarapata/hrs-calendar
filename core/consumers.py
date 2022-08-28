# chat/consumers.py
import json

from channels.generic.websocket import AsyncWebsocketConsumer


class AppConsumer(AsyncWebsocketConsumer):
    groups = ["main"]

    async def connect(self):
        self.group_name = self.scope["url_route"]["kwargs"]["group_name"]
        # Called on connection.
        # To accept the connection call:
        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()

    async def receive(self, text_data=None, bytes_data=None):
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]

        # Send message to group
        await self.channel_layer.group_send(
            self.group_name, {"type": "real_time_update", "message": message}
        )

    # Receive message from group
    async def real_time_update(self, event):
        message = event["message"]

        # Send message to WebSocket
        await self.send(text_data=json.dumps({"message": message}))

    async def disconnect(self, close_code):
        # Called when the socket closes
        await self.channel_layer.group_discard(self.group_name, self.channel_name)

