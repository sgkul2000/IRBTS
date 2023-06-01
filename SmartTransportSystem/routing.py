from django.urls import re_path

from . import socket

websocket_urlpatterns = [
    re_path(r"^ws/track/(?P<bus_no>\w+)/$", socket.TrackingConsumer.as_asgi()),
]