# Importing serializer methods:
from rest_framework import serializers

# Importing Database models:
from social_media_api.model_views_seralizers.reddit_api import reddit_models

# Abstract Serializer Objects:
class RedditPostsSerializer(serializers.HyperlinkedModelSerializer):
    
    # Explicitly Adding Primary Key to Reddit Serializer:
    id = serializers.CharField()

    def __init__(self, *args, **kwargs):
        many = kwargs.pop('many', True)
        super(RedditPostsSerializer, self).__init__(many=many, *args, **kwargs)

    class Meta:
        model = reddit_models.RedditPosts
        fields = "__all__"

