# Importing seralizer methods: 
from rest_framework import serializers

# Importing Youtube Database Models: 
from social_media_api.models.youtube.youtube_models import DailyYoutubeChannelStats

# Serializer for Daily Youtube Channel Statistics:
class DailyYoutubeChannelStatsSerializer(serializers.HyperlinkedModelSerializer):
    date_extracted = serializers.DateTimeField()
    class Meta:
        fields = "__all__"
        model = DailyYoutubeChannelStats 
