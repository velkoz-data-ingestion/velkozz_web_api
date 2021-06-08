# Importing Django packages:
from django.contrib import admin

# Importing News API models:
from news_api.model_views_seralizers.newspaper3k_articles.newspaper3k_models import NewsArticles

# Register your models here.
admin.site.register(NewsArticles)
