from django.urls import re_path

from . import socket

websocket_urlpatterns = [
    re_path(r"^ws/chat/$", socket.ChatConsumer.as_asgi()),
]