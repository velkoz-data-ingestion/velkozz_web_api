# Importing Django Models:
from django.contrib import admin

# Importing Database Models:
from .reddit_api_mvc.reddit_models import WallStreetBetsPosts, SciencePosts

# Registering the Reddit Posts Models to the Admin Dashboard:
admin.site.register(WallStreetBetsPosts)
admin.site.register(SciencePosts)