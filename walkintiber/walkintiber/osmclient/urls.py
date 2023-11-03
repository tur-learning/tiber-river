# osmclient/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('get_osm/', views.get_osm, name='get_osm'),  # Adjust as needed
    path('get_highways/', views.get_highways, name='get_highways'),  # Adjust as needed
    path('get_buildings/', views.get_buildings, name='get_buildings'),  # Adjust as needed
]
