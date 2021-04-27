# Importing base objects:
from accounts.views import AbstractModelViewSet

# Importing associated serializers/models:
from finance_api.models.structured_quant_data.wsb_data import WallStreetBetsTickerMentions
from finance_api.model_views_seralizers.structured_quant_data.wsb_data_serializers import WallStreetBetsTickerMentionsSerializer

class WallStreetBetsTickerMentionsViewSet(AbstractModelViewSet):
    """The ViewSets providing the REST API routes for the WallStreetBetsTickerMentions
    database table.
    """
    queryset = WallStreetBetsTickerMentions.objects.all()
    serializer_class = WallStreetBetsTickerMentionsSerializer
    
    def list(self, request):
        pass

    def create(self, request):
        pass