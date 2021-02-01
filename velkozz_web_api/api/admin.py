# Importing Django Models:
from django.contrib import admin

# Importing Database Models:
from .models import WallStreetBetsPosts, SciencePosts

# Registering the Reddit Posts Admin Models:
admin.site.register(WallStreetBetsPosts)
admin.site.register(SciencePosts)