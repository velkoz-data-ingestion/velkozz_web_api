# Importing Django Packages: 
from rest_framework import serializers

# Importing model methods: 
from news_api.model_views_seralizers.newspaper3k_articles.newspaper3k_views import NewsArticles


class NewsArticlesSeralizer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = NewsArticles
        fields = '__all__'