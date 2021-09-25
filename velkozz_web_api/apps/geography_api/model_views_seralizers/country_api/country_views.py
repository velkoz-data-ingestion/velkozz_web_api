# Importing Django Methods:
from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

# Importing the custom DjangoModelPermissions and ModelViewSets:
from accounts.views import AbstractModelViewSet

# Importing Data Management Packages:
import json

# Importing database models and seralizer objects:
from .country_models import Country
from .country_seralizers import CountrySerializer

# Country Summary Data Model View Set:
class CountryViewSet(AbstractModelViewSet):
    """
    The ModelViewSet for the Country data model. It writes and lists summary
    data about Countries written from REST countries. The ViewSet provides all
    of the CRUD operations for the Country data model and connects this model to
    the REST API. 
    """
    serializer_class = CountrySerializer
    queryset = Country.objects.all()
    
    def list(self, request):
        """The ViewSet method overwritten that contains the
        logic for processing GET requests from the generic post
        database table.   
        """
        # Creating context to be populated:
        context = {}
        context["request"] = request

        # Querying the country model:
        queryset = Country.objects.all()

        serializer = CountrySerializer(queryset, many=True, context=context)

        return Response(serializer.data)

    def create(self, request):
        """The ViewSet method that processes POST requests made to the
        Country Data API.


        The method de-seralizes the JSON payload and uses the bulk create-or-update
        django method to write to the Country Data Model.
        """
        # Creating a context dict to be populated:
        context = {}
        context["request"] = request

        # Attempting to extract payload from the request body:
        if request.body:
            country_data = json.loads(request.body)
        else:
            data = {} # Empty Json if no body content
    
        # Creating or updating the summary country data:
        country_summary_data = [
            Country.objects.update_or_create(
                common_name = data["name"]["common"],

                defaults = {
                    "names" : data["name"],
                    "topLevelDomain" : data.get("tld", None),
                    "alpha2Code" : data["cca2"],
                    "numericCode" : data.get("ccn3", None),
                    "alpha3Code" : data.get("cca3", None),
                    "cioc" : data.get("cioc", None),
                    "independent" : data.get("independent", None),
                    "status" : data["status"],
                    "unMember" : data["unMember"],
                    "currencies" : data.get("currencies", None),
                    "callingCodes" : data["idd"],
                    "capital" : data.get("capital", [None])[0],
                    "altSpellings" : data["altSpellings"],
                    "region" : data["region"],
                    "subregion" : data.get("subregion", None),
                    "languages" : data.get("languages", None),
                    "translations" : data["translations"],
                    "latlng" : data["latlng"],
                    "landlocked" : data["landlocked"],
                    "borders" : data.get("borders", None),
                    "area" : data["area"],
                    "demonym" : data.get("demonyms", None)
                }
            ) for data in country_data
        ]

        # Seralizing the objects that had been created:
        country_summary_data = [country_data[0] for country_data in country_summary_data]
        serializer = CountrySerializer(country_summary_data, many=True, context=context)

        return Response(serializer.data)
        