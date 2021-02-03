# Importing Django Methods:
from django.urls import include, path
from rest_framework import routers

# Importing the Reddit Views from the reddit_api_objs:
from .web_api_objs.reddit_api_objs import reddit_views

# Creating Url Router:
router = routers.DefaultRouter()

# Registering Reddit API routes:
router.register(r"reddit/rwallstreetbets", reddit_views.WallStreetBetsViewSets)
router.register(r"reddit/rscience", reddit_views.SciencePostsViewSets)

# Creating Automatic URL Routing:
urlpatterns = router.urls