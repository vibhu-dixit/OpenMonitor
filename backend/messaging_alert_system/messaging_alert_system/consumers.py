import json
from channels.generic.websocket import AsyncWebsocketConsumer
from inference_manager.views import get_inference
import cv2
import numpy as np
import requests

class VideoStreamConsumer(AsyncWebsocketConsumer):

    def convert_to_frame(self, bytes_data):
        # Convert bytes data to a video frame
        # This is a placeholder implementation
        try:
            np_array = np.frombuffer(bytes_data, np.uint8)
            frame = cv2.imdecode(np_array, cv2.IMREAD_COLOR)
            return frame
        except Exception as e:
            print(f"Error converting bytes to cv2 frame: {e}")
            return None

    async def connect(self):
        await self.accept()

    async def disconnect(self, close_code):
        pass

    async def receive(self, bytes_data):
        # Process the received video frame

        frame = self.convert_to_frame(bytes_data)
        if frame is None:
            return

        result = get_inference(frame)

        if not result:
            return

        data = {
            "message": "Intrusion detected!",
            "geo_coordinates": "(34.6556, 54.2339834)",
            "proof": result,
            "cam_number": 11
        }

        requests.post("http://localhost:8000/alert_api/v1/log/new/", json=data)

        await self.send(text_data=json.dumps({
            'message': 'Data received',
            'inference_result': result
        }))