# Importing DRF packages: 
from rest_framework import serializers

# Importing associated models: 
from finance_api.models.structured_quant_data.wsb_data import WallStreetBetsTickerMentions

class WallStreetBetsTickerMentionsSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = WallStreetBetsTickerMentions
        fields = "__all__"