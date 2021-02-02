# Importing Django Methods:
from django.urls import include, path
from rest_framework import routers
from . import views

# Creating Url Router:
router = routers.DefaultRouter()

# Registering Reddit API routes:
router.register(r"reddit/rwallstreetbets", views.WallStreetBetsViewSets)
router.register(r"reddit/rscience", views.SciencePostsViewSets)

# Creating Automatic URL Routing:
urlpatterns = router.urls