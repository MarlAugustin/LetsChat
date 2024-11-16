# chatapp/routing.py
from django.urls import path
from .consumers import chat_consumer
from . import views

websocket_urlpatterns = [
    path('ws/messages/<str:room_slug>/', chat_consumer.PublicChatConsumer.as_asgi()),
    path('ws/private-messages/<int:room_id>/', chat_consumer.PrivateChatConsumer.as_asgi()),
    # path('ws/online/', chat_consumer.OnlineStatusConsumer.as_asgi())
]