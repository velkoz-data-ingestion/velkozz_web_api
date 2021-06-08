# Importing Django Methods:
from django.urls import include, path
from rest_framework import routers

# Importing Newspaper3k MVC components:
from news_api.model_views_seralizers.newspaper3k_articles.newspaper3k_views import NewsArticlesViewSet

# Creating Url Router:
router = routers.DefaultRouter()

# Registering the endpoints for the Newspaper3k ViewSet: 
router.register(r"news_articles", NewsArticlesViewSet)

urlpatterns = router.urls