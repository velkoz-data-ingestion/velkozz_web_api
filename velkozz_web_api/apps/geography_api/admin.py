from django.contrib import admin

# Importing Country models:
from .model_views_seralizers.country_api.country_models import Country

# Registering Country data models:
admin.site.register(Country)
