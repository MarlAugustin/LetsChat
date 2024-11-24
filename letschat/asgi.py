"""
ASGI config for letschat project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application

from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter

import chat.routing 
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'letschat.settings')

# asgi.py file is used to define the application for the ASGI protocol.
# This way we can use Django Channels to handle WebSockets.
# It's important, because without it we wouldn't be able to send messages in real-time.
http_response_app = get_asgi_application()
application = ProtocolTypeRouter({
    "http": http_response_app,
    "websocket": AuthMiddlewareStack( 
        URLRouter(
            chat.routing.websocket_urlpatterns
        ))
})
