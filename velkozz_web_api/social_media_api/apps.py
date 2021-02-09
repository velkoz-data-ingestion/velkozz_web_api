# Importing Django packages:
from django.apps import AppConfig, apps
from django.contrib.auth.management import create_permissions
#from django.contrib.contenttypes.models import ContentType

class SocialMediaAPIConfig(AppConfig):
    name = 'social_media_api'
    verbose_name = "Social Media Data API"        



