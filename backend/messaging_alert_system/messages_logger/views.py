from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Message
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
        alerts = Message.objects.all()
        return Response(alerts, status=status.HTTP_200_OK)
    return Response(status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def get_unaddressed_alerts(request):
    if request.method == 'GET':
        alerts = Message.objects.filter(alert_addressed=False)
        return Response(alerts, status=status.HTTP_200_OK)
    return Response(status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def mark_alert_addressed(request, alert_id):
    if request.method == 'POST':
        alert = Message.objects.get(id=alert_id)
        confirm_image = request.data.get('confirm_image')
        alert.confirmation = confirm_image
        alert.alert_addressed = True
        alert.save()
        return Response(status=status.HTTP_200_OK)
    return Response(status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def get_alert_by_id(request, alert_id):
    if request.method == 'GET':
        alert = Message.objects.get(id=alert_id)
        return Response(alert, status=status.HTTP_200_OK)
    return Response(status=status.HTTP_400_BAD_REQUEST)

