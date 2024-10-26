# chatapp/routing.py
from django.urls import path
from .consumers import chat_consumer
from . import views

websocket_urlpatterns = [
    path('ws/messages/<str:room_slug>/', chat_consumer.ChatConsumer.as_asgi()),
]