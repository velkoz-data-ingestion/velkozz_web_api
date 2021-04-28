# Importing base objects:
from accounts.views import AbstractModelViewSet

# Importing associated serializers/models:
from finance_api.models.structured_quant_data.wsb_data import WallStreetBetsTickerMentions
from finance_api.model_views_seralizers.structured_quant_data.wsb_data_serializers import WallStreetBetsTickerMentionsSerializer

# Importing data managment packages:
import json

# Importing DRF packages::
from rest_framework.response import Response

class WallStreetBetsTickerMentionsViewSet(AbstractModelViewSet):
    """The ViewSets providing the REST API routes for the WallStreetBetsTickerMentions
    database table.
    """
    queryset = WallStreetBetsTickerMentions.objects.all()
    serializer_class = WallStreetBetsTickerMentionsSerializer
    
    def list(self, request):
        """The ViewSet method that processes GET requests made to the
        WallStreetBetsTickerMentions API.

        It extracts ticker frequency mentions from the database, seralizes it 
        into a JSON format and sends it as the body in a GET request.
        """
        context = {}
        context["request"] = request

        # Querying the database ticker mentions:
        ticker_mentions = WallStreetBetsTickerMentions.objects.all()
        seralized_data = WallStreetBetsTickerMentionsSerializer(ticker_mentions, many=True, context=context)

        return Response(seralized_data.data)

    def create(self, request):
        """The ViewSet method that processes POST requests made to the
        WallStreetBetsTickerMentions API.


        The method de-seralizes the JSON payload and uses the bulk create-or-update
        django method to write ticker frequency counts to the database.
        """
        # Extracting content from the request body:
        if request.body:

            # Loading request body content:
            body_content = json.loads(request.body)
            
            # Assumes data in the format [{date:{}}, {date:{}}, {date:{}}]
            # Writing data to the database/updating existing entries:
            ticker_freq_counts = [
                WallStreetBetsTickerMentions.objects.update_or_create(
                    day = ticker_freq_dict["day"],

                    defaults = {
                        "ticker_count": ticker_freq_dict["freq_counts"]
                    }
                
                ) for ticker_freq_dict in body_content]
            
            return Response(body_content)
            
