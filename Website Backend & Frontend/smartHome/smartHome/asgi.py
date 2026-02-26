# """
# ASGI config for smartHome project.

# It exposes the ASGI callable as a module-level variable named ``application``.

# For more information on this file, see
# https://docs.djangoproject.com/en/5.2/howto/deployment/asgi/
# """

# import os

# from django.core.asgi import get_asgi_application

# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'smartHome.settings')

# django_asgi_app = get_asgi_application()

# from channels.routing import ProtocolTypeRouter , URLRouter
# from channels.security.websocket import AllowedHostsOriginValidator
# from esp32 import routing




# application = ProtocolTypeRouter ({
#     "http" : django_asgi_app ,
#     "websocket" :URLRouter(routing.websocket_urlpatterns),
# })


import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'smartHome.settings')

asgi_application = get_asgi_application()

from esp32 import routing
application = ProtocolTypeRouter({
    "http": asgi_application,
    "websocket": URLRouter(routing.websocket_urlpatterns),
})
