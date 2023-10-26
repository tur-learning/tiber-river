from django.apps import AppConfig
# import os


class OsmclientConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'osmclient'

    # def ready(self):
    #     # Code to be executed when the app is ready
    #     ASSETS_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'assets/osm')
    #     os.makedirs(ASSETS_DIR, exist_ok=True)