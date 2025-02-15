from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import log_alert, get_alerts, get_unaddressed_alerts, mark_alert_addressed, get_alert_by_id

app_name = "messages_logger"
urlpatterns =[
    path('log/new/', log_alert, name='log_alert'),
    path('logs/alerts/<int:alert_id>/', get_alert_by_id, name='get_alert_by_id'),
    path('logs/alerts/', get_alerts, name='get_alerts'),
    path('logs/alerts/unaddressed/', get_unaddressed_alerts, name='get_unaddressed_alerts'),
    path('logs/alerts/<int:alert_id>/mark_addressed/', mark_alert_addressed, name='mark_alert_addressed'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)