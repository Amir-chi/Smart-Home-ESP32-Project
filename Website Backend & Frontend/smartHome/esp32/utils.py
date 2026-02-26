from channels.layers import get_channel_layer
from django.core.cache import cache
import base64
from asgiref.sync import async_to_sync
import json
import logging


logger = logging.getLogger(__name__)


from .models import LedStatus


LED_STATUS_MAP = {
    "flash_on":  ("led0", "on"),
    "flash1_on": ("led1", "on"),
    "flash2_on": ("led2", "on"),
    "flash3_on": ("led3", "on"),
    "flash_off":  ("led0", "off"),
    "flash1_off": ("led1", "off"),
    "flash2_off": ("led2", "off"),
    "flash3_off": ("led3", "off"),
}

def set_led_status(status: str) -> None:
    mapping = LED_STATUS_MAP.get(status)
    if not mapping:
        logger.warning(f"Unknown LED status command: {status}")
        return
    
    led_name, led_status = mapping
    LedStatus.objects.filter(led_name=led_name).update(led_status=led_status)
  
        

async def send_image_to_group(group_name, image_file):
    print("ready for send image to group")
    channel_layer = get_channel_layer()
    
    image_data = base64.b64encode(image_file.read()).decode('utf-8')
    
    async_to_sync(channel_layer.group_send)(
        group_name,
        {
            'type': 'send_image',
            'image': image_data,
        }
    )
    
    print("image sent to group")
    
    

def process_and_send_commands(command: str, channel_layer) -> None:
    lines = command.strip().splitlines()
    commands = lines if len(lines) > 1 else [command]
    
    for cmd in commands:
        
        try:
            data = json.loads(cmd)
            
        except json.JSONDecodeError:
            logger.warning(f"Invalid JSON skipped: {cmd}")
            continue
        
        if "flash" in data.get("action", ""):
            set_led_status(data["action"])
            
        async_to_sync(channel_layer.group_send)(
            'chat',
            {'type': 'message',
             'message': cmd}
        )