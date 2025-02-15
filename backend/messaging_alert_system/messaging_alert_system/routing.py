from django.urls import path
from .consumers import VideoStreamConsumer

websocket_urlpatterns = [
    path('ws/video/', VideoStreamConsumer.as_asgi()),
]