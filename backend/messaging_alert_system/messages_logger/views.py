from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Message
from zone_manager.models import Zone
# Create your views here.

@api_view(['POST'])
def log_alert(request):

    if request.method == 'POST':
        message = request.data.get('message')
        geo_coordinates = request.data.get('geo_coordinates')
        proof = request.data.get('proof')
        alert_zone = request.data.get('alert_zone')
        Message.objects.create(message=message, geo_coordinates=geo_coordinates, proof=proof, alert_zone=alert_zone)
        return Response(status=status.HTTP_201_CREATED)
    return Response(status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def get_alerts(request):
    if request.method == 'GET':
        alerts =  None
        if request.user.groups.filter(name='Admin').exists():
            alerts = Message.objects.all()
        else:
            zone = request.data.get('zone')
            alerts = Message.objects.filter(alert_zone=zone)
        return Response(alerts.values(), status=status.HTTP_200_OK)
    return Response(status=status.HTTP_400_BAD_REQUEST)
