# Importing Django Methods:
from django.urls import include, path
from rest_framework import routers

# Importing Country Views:
from geography_api.model_views_seralizers.country_api.country_views import CountryViewSet

# Creating Url Routers:
router = routers.DefaultRouter()

# Adding Endpoints for Country Summary Data:
router.register(r"countries/summary", CountryViewSet)

# Creating Automatic URL Routing:
urlpatterns = router.urls
