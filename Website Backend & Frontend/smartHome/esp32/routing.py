from django.urls import re_path

from esp32 import consumers


websocket_urlpatterns = [
    re_path(r'ws/message/', consumers.Esp32Consumer.as_asgi()),
    re_path(r'ws/bot_connection/', consumers.BotConsumer.as_asgi()),
]