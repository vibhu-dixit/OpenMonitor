from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Zone(models.Model):
    zone_name = models.CharField(max_length=200)
    associated_users = models.ManyToManyField('User', related_name='zoneWorkers')
    alert_count = models.BigIntegerField()
    associated_rangers = models.ManyToManyField('User', related_name='zoneRangers')

    def __str__(self):
        return f"{self.zone_name} | alert count: {self.alert_count}"

