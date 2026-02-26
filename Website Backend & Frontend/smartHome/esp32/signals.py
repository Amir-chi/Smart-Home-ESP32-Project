from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.cache import cache
import logging
from django.db.models.signals import post_migrate
from django.dispatch import receiver
import base64
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer

logger = logging.getLogger(__name__)

from .models import Esp32Picture


@receiver(post_save, sender=Esp32Picture)
def photo_saved_handler(sender, instance, created, **kwargs):
    if created:
        if cache.get("is_bot_online"):
        
            channel_layer = get_channel_layer()

            image_data = base64.b64encode(instance.image.read()).decode('utf-8')
            
            async_to_sync(channel_layer.group_send)(
                "bot_group",
                {
                    'type': 'send_image',
                    'image': image_data,
                }
            )

            async_to_sync(channel_layer.group_send)(
                    "bot_group",
                    {
                        'type': 'send_text',
                        'message': 'close',
                    }
                )

                
                
                

LED_NAMES = ["led0", "led1", "led2", "led3"]

@receiver(post_migrate)
def initialize_led_status(sender, **kwargs):
    if sender.name == "esp32":  
        from .models import LedStatus
        for led_name in LED_NAMES:
            _, created = LedStatus.objects.get_or_create(
                led_name=led_name,
                defaults={"led_status": "off"}
            )
            if created:
                logger.info(f"LED {led_name} initialized.")
