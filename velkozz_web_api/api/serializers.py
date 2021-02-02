# Importing serializer methods:
from rest_framework import serializers

# Importing Database models:
from .models import WallStreetBetsPosts, SciencePosts

# Abstract Serializer Objects:
class RedditPostsSerializer(serializers.HyperlinkedModelSerializer):
    
    # Explicitly Adding Primary Key to Reddit Serializer:
    id = serializers.CharField()

    def __init__(self, *args, **kwargs):
        many = kwargs.pop('many', True)
        super(RedditPostsSerializer, self).__init__(many=many, *args, **kwargs)

    class Meta:
        fields = "__all__"

# Reddit Posts Serializers:
class WallStreetBetsSerializer(RedditPostsSerializer):
    class Meta(RedditPostsSerializer.Meta):
        model = WallStreetBetsPosts
        

class SciencePostsSerializer(RedditPostsSerializer):
    class Meta(RedditPostsSerializer.Meta):
        model = SciencePosts

