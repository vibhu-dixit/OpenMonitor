from django.urls import path
from .consumers import VideoStreamConsumer

websocket_urlpatterns = [
    path('ws/stream/', VideoStreamConsumer.as_asgi()),
]