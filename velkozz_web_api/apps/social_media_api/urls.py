# Importing Django Methods:
from django.urls import include, path
from rest_framework import routers

# Importing the Reddit Views from the Reddit MVC:
from .model_views_seralizers.reddit_api import reddit_views

# Creating Url Router:
router = routers.DefaultRouter()

# Registering Reddit API routes:
router.register(r"reddit/rwallstreetbets", reddit_views.WallStreetBetsViewSet)
router.register(r"reddit/rscience", reddit_views.SciencePostsViewSet)
router.register(r"reddit/rworldnews", reddit_views.WorldNewsViewSet)

# Creating Automatic URL Routing:
urlpatterns = router.urls
    
