from django.db import models

# Create your models here.
class SensorEvent(models.Model):
    device_id = models.CharField(max_length=50, default="esp32_1")
    response_time = models.DateTimeField(auto_now_add=True)
    distance_value = models.FloatField()

    def __str__(self):
        return f"Get new response: at {self.response_time}, distance {self.distance_value}"
