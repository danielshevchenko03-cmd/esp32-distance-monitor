import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from .models import SensorEvent

# Create your views here.
@csrf_exempt
def get_esp_data(request):
    if request.method == "POST":
        data = json.loads(request.body)
        distance = data["distance"]
        device_id = data.get("device_id", "esp32_1")

        event = SensorEvent(distance_value=distance, device_id=device_id)
        event.save()
        return JsonResponse({"status": "ok"})
    
    else:
        return JsonResponse({"error": "Only POST requests!"}, status=405)

def export_data(request):
    events = SensorEvent.objects.all()
    results = []

    for event in events:
        results.append({"id": event.id, 
                        "device_id": event.device_id,
                        "time": event.response_time.strftime("%Y-%m-%d %H:%M:%S"),
                        "distance": event.distance_value})

    return JsonResponse(results, safe=False)