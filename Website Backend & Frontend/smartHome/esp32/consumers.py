import json
import uuid
import logging

from channels.generic.websocket import AsyncWebsocketConsumer
from django.core.files.base import ContentFile
from django.core.cache import cache
from asgiref.sync import sync_to_async

from .models import Esp32Picture, CommandHistory

logger = logging.getLogger(__name__)


CHAT_GROUP = "chat"
BOT_GROUP = "bot_group"

class Esp32Consumer(AsyncWebsocketConsumer):
    
    async def connect(self):
        self.chat_group_name = CHAT_GROUP
  
        await self.channel_layer.group_add(
            self.chat_group_name,
            self.channel_name
        )
        
        await self.accept()

        await self._broadcast_status("connected")
        
        
    async def disconnect(self, code):
        
        if hasattr(self , "chat_group_name"):
            
            await self.channel_layer.group_send(
                self.chat_group_name,
                {
                    'type': 'status',
                    'message': {
                        'type': 'disconnected',
                    }
                }
            )
            
            await self.channel_layer.group_discard(
                self.chat_group_name,
                self.channel_name
            )
        
        logger.info(f"WebSocket disconnected: {code}")

        

    async def receive(self, text_data = None , bytes_data = None):
        try :
            
            if bytes_data:
                
                await self._handle_bytes(bytes_data)
                return
                
            if text_data:
                await self._handle_text(text_data)
        except Exception as e:
            logger.exception(f"Error in receive: {e}")
            
            
    async def _handle_bytes(self, bytes_data):
        
        file_name = f"upload_{uuid.uuid4().hex[:8]}.jpg"
        image_file = ContentFile(bytes_data, name=file_name)
        
        picture = await Esp32Picture.objects.acreate(image=image_file)
        
        await self.send(text_data=json.dumps({
            "status": "success",
            "filename": picture.image.name,
        }))

    async def _handle_text(self, text_data):
        try:
            data = json.loads(text_data)
        except json.JSONDecodeError:
            await self.send(text_data=json.dumps({"type": "error", "message": "Invalid JSON"}))
            return

        message_type = data.get("type")
        if message_type == "message":
            await self.handle_message(data)


    async def handle_message(self , data):
        try:
            content = data.get("message" , "").strip()
            if not content:
                return
            
            await self.channel_layer.group_send(
                self.chat_group_name,
                {
                    "type" : "message",
                    "message" : {
                        "type" : "new_message",
                        "data" : content
                    }
                }
            )
        except Exception as e:    
            logger.exception(f"Error in handle message: {e}")
            
    

    async def message(self, event):
        try:
            
            command = str(event["message"])
            
            await CommandHistory.objects.acreate(command=command)
            
            await self.send(text_data=json.dumps(event['message']))
            
        except Exception as e:
            logger.exception(f"Error in message handler: {e}")
            
            
    async def status(self, event):
        await self.send(text_data=json.dumps(event['message']))
        
    async def _broadcast_status(self, action: str):
        await self.channel_layer.group_send(
            self.chat_group_name,
            {"type": "status", "message": {"action": action}},
        )

        
class BotConsumer(AsyncWebsocketConsumer):
    
    async def connect(self):    

        await self.channel_layer.group_add(BOT_GROUP, self.channel_name)

        await self.accept()

        await sync_to_async(cache.set)("is_bot_online", True, 3600)  
        
        await self.channel_layer.group_send(
            BOT_GROUP,
            {
                'type': 'send_text',
                'content': {
                'َaction': 'connected',

            }
        }
        )

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(BOT_GROUP, self.channel_name)
        cache.set("is_bot_online", False)

    async def send_text(self, event):
        
        content = event.get("content")

        if content:
            await self.send(text_data=json.dumps(content))

    async def send_image(self, event):
    
        await self.send(text_data=json.dumps({
            'type': 'new_image',
            'image': event['image'],
        }))
        
        

