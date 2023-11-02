# osmclient/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('get_osm/', views.get_osm, name='get_osm'),  # Adjust as needed
    path('get_osm_relations_ways/', views.get_osm_relations_ways, name='get_osm_relations_ways'),  # Adjust as needed
    path('post_osm_relations_ways/', views.post_osm_relations_ways, name='post_osm_relations_ways'),  # Adjust as needed
    path('get_osm_highways/', views.get_osm_highways, name='get_osm_highways'),  # Adjust as needed
]
