from django.urls import path
from . import views

urlpatterns = [
    path("esp-data/", views.get_esp_data, name="get data"),
    path("events/", views.export_data, name="send list"),
]
