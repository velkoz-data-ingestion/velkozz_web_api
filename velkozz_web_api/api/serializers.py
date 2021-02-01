# Importing serializer methods:
from rest_framework import serializers

# Importing Database models:
from .models import WallStreetBetsPosts, SciencePosts

# Abstract Serializer Objects:
class RedditPostsSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        fields = "__all__"

# Reddit Posts Serializers:
class WallStreetBetsSerializer(RedditPostsSerializer):
    class Meta(RedditPostsSerializer.Meta):
        model = WallStreetBetsPosts
        

class SciencePostsSerializer(RedditPostsSerializer):
    class Meta(RedditPostsSerializer.Meta):
        model = SciencePosts