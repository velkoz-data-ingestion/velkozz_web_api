# Importing serializer methods:
from rest_framework import serializers

# Importing Database Models:
from social_media_api.models.indeed.indeed_models import IndeedJobPosts

class IndeedJobsPostsSerializer(serializers.HyperlinkedModelSerializer):
    """The hyperlink seralizer for Indeed Job Posts.
    """
    # Explicitly Adding Primary Key to Indeed Jobs Serializer:
    id = serializers.CharField()
    class Meta:
        model = IndeedJobPosts
        fields = "__all__"
