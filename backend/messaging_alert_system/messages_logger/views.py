from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Message
from datetime import datetime
import uuid
# Create your views here.

def gen_uuid():
    return uuid.uuid4().hex


@api_view(['POST'])
def log_alert(request):
    if request.method == 'POST':
        message = request.data.get('message')
        geo_coordinates = request.data.get('geo_coordinates')
        proof = request.data.get('proof')
        cam_number = request.data.get('cam_number')
        Message.objects.create(message=message, geo_coordinates=geo_coordinates, proof=proof, timestamp=datetime.now(), camera_number=cam_number)
        return Response(data={"message":"Alert created!"}, status=status.HTTP_201_CREATED)
    return Response(status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def get_alerts(request):
    if request.method == 'GET':
        alerts = Message.objects.all()
        return Response(alerts.values(), status=status.HTTP_200_OK)
    return Response(status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def get_unaddressed_alerts(request):
    if request.method == 'GET':
        alerts = Message.objects.filter(alert_addressed=False)
        return Response(alerts.values(), status=status.HTTP_200_OK)
    return Response(status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def mark_alert_addressed(request, alert_id):
    if request.method == 'POST':
        alert = Message.objects.get(id=alert_id)
        confirm_image = request.data.get('confirm_image')
        ext = confirm_image.name.split('.')[-1]
        confirm_image.name = f"{gen_uuid()}." + ext
        alert.confirmation = confirm_image
        alert.alert_in_progress = False
        alert.alert_addressed = True
        alert.save()
        return Response(data={"message": "Alert addressed!"}, status=status.HTTP_200_OK)
    return Response(status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def mark_alert_in_progress(request, alert_id):
    if request.method == 'POST':
        alert = Message.objects.get(id=alert_id)
        alert.alert_in_progress = True
        alert.alert_addressed = False
        alert.save()
        return Response(data={"message":"Ranger assigned!"}, status=status.HTTP_200_OK)
    return Response(status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def get_alert_by_id(request, alert_id):
    if request.method == 'GET':
        alert = Message.objects.get(id=alert_id)
        data = {
            "message": alert.message,
            "timestamp": alert.timestamp,
            "geo_coordinates": alert.geo_coordinates,
            "proof": alert.proof.url,
            "alert_addressed": alert.alert_addressed,
            "alert_in_progress": alert.alert_in_progress,
            "confirmation": alert.confirmation.url if alert.confirmation else None,
        }
        return Response(data, status=status.HTTP_200_OK)
    return Response(status=status.HTTP_400_BAD_REQUEST)

