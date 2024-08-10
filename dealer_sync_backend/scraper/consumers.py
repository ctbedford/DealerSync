import json
import logging
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.exceptions import DenyConnection

logger = logging.getLogger(__name__)


class SyncConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        try:
            self.user = self.scope.get("user")
            if not self.user or not self.user.is_authenticated:
                raise DenyConnection("User is not authenticated")

            self.sync_group_name = f'sync_{self.user.id}'
            logger.info(f"WebSocket connection attempt for user {
                        self.user.id}")

            # Join sync group
            await self.channel_layer.group_add(
                self.sync_group_name,
                self.channel_name
            )
            logger.info(f"User {self.user.id} added to group {
                        self.sync_group_name}")
            await self.accept()
        except Exception as e:
            logger.error(f"Error in connect: {str(e)}")
            raise

    async def disconnect(self, close_code):
        try:
            if hasattr(self, 'sync_group_name'):
                # Leave sync group
                await self.channel_layer.group_discard(
                    self.sync_group_name,
                    self.channel_name
                )
                logger.info(f"User {self.user.id} disconnected from group {
                            self.sync_group_name}")
        except Exception as e:
            logger.error(f"Error in disconnect: {str(e)}")

    async def receive(self, text_data):
        try:
            text_data_json = json.loads(text_data)
            message = text_data_json['message']
            logger.info(f"Received message from user {
                        self.user.id}: {message}")

            # Send message to sync group
            await self.channel_layer.group_send(
                self.sync_group_name,
                {
                    'type': 'sync_message',
                    'message': message
                }
            )
        except Exception as e:
            logger.error(f"Error in receive: {str(e)}")

    async def sync_message(self, event):
        try:
            message = event['message']
            logger.info(f"Sending message to user {self.user.id}: {message}")

            # Send message to WebSocket
            await self.send(text_data=json.dumps({
                'message': message
            }))
        except Exception as e:
            logger.error(f"Error in sync_message: {str(e)}")
