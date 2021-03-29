# Importing serializer methods:
from rest_framework import serializers

# Importing Database models:
from social_media_api.models.reddit import reddit_models
# Abstract Serializer Objects:
class RedditPostsSerializer(serializers.HyperlinkedModelSerializer):
    
    # Explicitly Adding Primary Key to Reddit Serializer:
    id = serializers.CharField()
    subreddit = serializers.CharField()

    def __init__(self, *args, **kwargs):
        many = kwargs.pop('many', True)
        super(RedditPostsSerializer, self).__init__(many=many, *args, **kwargs)

    class Meta:
        model = None
        fields = "__all__"

# Reddit Posts Serializers:
class WallStreetBetsPostsSerializer(RedditPostsSerializer):
    class Meta(RedditPostsSerializer.Meta):
        model = reddit_models.WallStreetBetsPosts
        
class SciencePostsSerializer(RedditPostsSerializer):
    class Meta(RedditPostsSerializer.Meta):
        model = reddit_models.SciencePosts

class WorldNewsPostsSerializer(RedditPostsSerializer):
    class Meta(RedditPostsSerializer.Meta):
        model = reddit_models.WorldNewsPosts

class NewsPostsSerializer(RedditPostsSerializer):
    class Meta(RedditPostsSerializer.Meta):
        model = reddit_models.NewsPosts

class EnergyPostsSerializer(RedditPostsSerializer):
    class Meta(RedditPostsSerializer.Meta):
        model = reddit_models.EnergyPosts

class EconomicsPostsSerializer(RedditPostsSerializer):
    class Meta(RedditPostsSerializer.Meta):
        model = reddit_models.EconomicsPosts

class PoliticsPostsSerializer(RedditPostsSerializer):
    class Meta(RedditPostsSerializer.Meta):
        model = reddit_models.PoliticsPosts

class CanadaPostsSerializer(RedditPostsSerializer):
    class Meta(RedditPostsSerializer.Meta):
        model = reddit_models.CanadaPosts

class UKPoliticsPostsSerializer(RedditPostsSerializer):
    class Meta(RedditPostsSerializer.Meta):
        model = reddit_models.UKPoliticsPosts

class PalestinePostsSerializer(RedditPostsSerializer):
    class Meta(RedditPostsSerializer.Meta):
        model = reddit_models.PalestinePosts

class MiddleEastNewsPostsSerializer(RedditPostsSerializer):
    class Meta(RedditPostsSerializer.Meta):
        model = reddit_models.MiddleEastNewsPosts

class IsraelPostsSerializer(RedditPostsSerializer):
    class Meta(RedditPostsSerializer.Meta):
        model = reddit_models.IsraelPosts

class PakistanPostsSerializer(RedditPostsSerializer):
    class Meta(RedditPostsSerializer.Meta):
        model = reddit_models.PakistanPosts
    
class IndiaPostsSerializer(RedditPostsSerializer):
    class Meta(RedditPostsSerializer.Meta):
        model = reddit_models.IndiaPosts

class LiberalPostsSerializer(RedditPostsSerializer):
    class Meta(RedditPostsSerializer.Meta):
        model = reddit_models.LiberalPosts

class ConservativePostsSerializer(RedditPostsSerializer):
    class Meta(RedditPostsSerializer.Meta):
        model = reddit_models.ConservativePosts

class SocialismPostsSerializer(RedditPostsSerializer):
    class Meta(RedditPostsSerializer.Meta):
        model = reddit_models.SocialismPosts

class ProgressivePostsSerializer(RedditPostsSerializer):
    class Meta(RedditPostsSerializer.Meta):
        model = reddit_models.ProgressivePosts

class DemocratsPostsSerializer(RedditPostsSerializer):
    class Meta(RedditPostsSerializer.Meta):
        model = reddit_models.DemocratsPosts

class LiberalPostsSerializer(RedditPostsSerializer):
    class Meta(RedditPostsSerializer.Meta):
        model = reddit_models.LiberalPosts

class TechnologyPostsSerializer(RedditPostsSerializer):
    class Meta(RedditPostsSerializer.Meta):
        model = reddit_models.TechnologyPosts

class RealTechPostsSerializer(RedditPostsSerializer):
    class Meta(RedditPostsSerializer.Meta):
        model = reddit_models.RealTechPosts

class TechPostsSerializer(RedditPostsSerializer):
    class Meta(RedditPostsSerializer.Meta):
        model = reddit_models.TechPosts

class NeutralPoliticsPostsSerializer(RedditPostsSerializer):
    class Meta(RedditPostsSerializer.Meta):
        model = reddit_models.NeutralPoliticsPosts

class ChinaPostsSerializer(RedditPostsSerializer):
    class Meta(RedditPostsSerializer.Meta):
        model = reddit_models.ChinaPosts

class TaiwanPostsSerializer(RedditPostsSerializer):
    class Meta(RedditPostsSerializer.Meta):
        model = reddit_models.TaiwanPosts

class JapanPostsSerializer(RedditPostsSerializer):
    class Meta(RedditPostsSerializer.Meta):
        model = reddit_models.JapanPosts

class KoreaPostsSerializer(RedditPostsSerializer):
    class Meta(RedditPostsSerializer.Meta):
        model = reddit_models.KoreaPosts

class SingaporePostsSerializer(RedditPostsSerializer):
    class Meta(RedditPostsSerializer.Meta):
        model = reddit_models.SingaporePosts

class MalaysiaPostsSerializer(RedditPostsSerializer):
    class Meta(RedditPostsSerializer.Meta):
        model = reddit_models.MalaysiaPosts

class ThailandPostsSerializer(RedditPostsSerializer):
    class Meta(RedditPostsSerializer.Meta):
        model = reddit_models.ThailandPosts

class NorthKoreaPostsSerializer(RedditPostsSerializer):
    class Meta(RedditPostsSerializer.Meta):
        model = reddit_models.NorthKoreaPosts

class NorthKoreaNewsPostsSerializer(RedditPostsSerializer):
    class Meta(RedditPostsSerializer.Meta):
        model = reddit_models.NorthKoreaNewsPosts

class ConflictNewsPostsSerializer(RedditPostsSerializer):
    class Meta(RedditPostsSerializer.Meta):
        model = reddit_models.ConflictNewsPosts

class HongKongPostsSerializer(RedditPostsSerializer):
    class Meta(RedditPostsSerializer.Meta):
        model = reddit_models.HongKongPosts

class SpacePostsSerializer(RedditPostsSerializer):
    class Meta(RedditPostsSerializer.Meta):
        model = reddit_models.SpacePosts

class CryptoCurrencyPostsSerializer(RedditPostsSerializer):
    class Meta(RedditPostsSerializer.Meta):
        model = reddit_models.CryptoCurrencyPosts
