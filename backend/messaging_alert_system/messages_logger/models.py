from django.db import models

# Create your models here.
class Message(models.Model):
    message = models.CharField(max_length=200)
    timestamp = models.DateTimeField(auto_now_add=True)
    geo_coordinates = models.CharField(max_length=200)
    proof = models.ImageField(upload_to='proofs/')
    confirmation = models.ImageField(upload_to='confirmations/', null=True, blank=True)
    alert_addressed = models.BooleanField(default=False)
    alert_in_progress = models.BooleanField(default=False)
    camera_number = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.message} logged \n at {self.timestamp} \n at {self.geo_coordinates} \n"

