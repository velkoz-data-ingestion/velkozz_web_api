# Importing Django Models:
from django.contrib import admin

# Importing Database Models:
from .models.reddit.reddit_models import WallStreetBetsPosts, SciencePosts

# Registering the Reddit Posts Models to the Admin Dashboard:
admin.site.register(WallStreetBetsPosts)
admin.site.register(SciencePosts)