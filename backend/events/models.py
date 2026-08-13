from django.db import models

# Create your models here.
class SensorEvent(models.Model):
    response_time = models.DateTimeField(auto_now_add=True)
    distance_value = models.FloatField()

    def __str__(self):
        return f"Get new response: at {self.response_time}, distance {self.distance_value}"
