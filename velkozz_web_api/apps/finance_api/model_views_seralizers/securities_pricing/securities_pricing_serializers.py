# DRF Packages:
from rest_framework import serializers

# Importing Associated db models:
from finance_api.models.securities_data.securities_ohlc import SecurityPriceOHLC

class SecuritiesPriceOHLCSerializer(serializers.HyperlinkedModelSerializer):
    """Seralizer that Seralizes the files necessary for populating the Security
    OHLC database model.
    """
    ticker = serializers.CharField()
    ohlc_csv = serializers.FileField()

    class Meta:
        model = SecurityPriceOHLC
