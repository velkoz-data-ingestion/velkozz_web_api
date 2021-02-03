# Importing Django Models:
from django.contrib import admin

# Importing Database models post:
from .web_api_objs.reddit_api_objs.reddit_models import WallStreetBetsPosts, SciencePosts

# Registering the Reddit Posts Admin Models:
admin.site.register(WallStreetBetsPosts)
admin.site.register(SciencePosts)