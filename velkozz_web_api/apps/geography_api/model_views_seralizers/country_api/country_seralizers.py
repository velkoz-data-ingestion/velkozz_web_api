# Importing serializer methods:
from rest_framework import serializers

# Importing Country models:
from geography_api.model_views_seralizers.country_api.country_models import Country

# Serializer for Country summary data model:
class CountrySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        fields = "__all__"
        model = Country
