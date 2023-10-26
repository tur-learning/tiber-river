# osmclient/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('get_osm/', views.get_osm, name='get_osm'),  # Adjust as needed
]
