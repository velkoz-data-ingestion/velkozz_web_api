# Importing Django Methods:
from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import Permission 

# Importing Data Management Packages:
import json

# Importing the Market Index Seralizers, Database Models and Base ModelViewSets:
from accounts.views import AbstractModelViewSet
from finance_api.models.market_indicies.market_indicies_models import * 
from .market_indicies_serializers import * 

# Market Indicies ModelViewSet
class SPYIndexCompositionViewSet(AbstractModelViewSet):
    """The ViewSets providing the REST API routes for the SPYIndexComposition
    database table.
    """
    queryset = SPYIndexComposition.objects.all()
    serializer_class = SPYIndexSerializer

    def list(self, request):
        """The ViewSet method overwritten that contains the logic for processing GET requests
        to the SPY Index database table. 
        """
        # Creating a context dict to be populated:
        context = {}
        context['request'] = request
                
        # Querying all of the data from the database:
        queryset = SPYIndexComposition.objects.all()
        serializer = SPYIndexSerializer(queryset, many=True, context=context)

        return Response(serializer.data)
    
    def create(self, request):
        """The ViewSet method that contains logic for processing POST requests
        to the SPY Index database table.
        """
        # Creating a context dict to be populated:
        context = {}
        context['request'] = request
        
        queryset = SPYIndexComposition.objects.all()
        serializer = SPYIndexSerializer(queryset, many=True, context=context)

        # Extracting the json content from the request body:
        if request.body:
            
            # Loading all data from the request body:
            body_content = json.loads(request.body)

            # Creating or Updating existing model instance via list comprehension:
            django_objs_lst = [
                SPYIndexComposition.objects.update_or_create(
                    cik= json["CIK"],

                    defaults = {
                        "symbol" : json["Symbol"],
                        "security_name" : json["Security"],
                        'gics_sector' : json["GICS Sector"], 
                        'gics_sub_industry' : json["GICS Sub-Industry"],
                        'headquarters_location' : json["Headquarters Location"],
                        'date_added' : json["Date first added"],
                        'founded' : json["Founded"]}
                    
                    ) for json in body_content]            
                
        return Response(serializer.data)

class DJIAIndexCompositionViewSet(AbstractModelViewSet):
    """The ViewSets providing the REST API routes for the DJIAIndexComposition
    database table.
    """
    queryset = DJIAIndexComposition.objects.all()
    serializer_class = DJIAIndexSerializer

    def list(self, request):
        """Method that contains logic for processing GET request to the
        DJIA Index database table.
        """
        # Creating a context dict to be populated:
        context = {}
        context['request'] = request

        # Querying all of the data from the database:
        queryset = DJIAIndexComposition.objects.all()
        serializer = DJIAIndexSerializer(queryset, many=True, context=context)

        return Response(serializer.data)

    def create(self, request):
        """The ViewSet method that contains logic for processing POST requests
        to the DJIA Index database table.
        """
        # Creating a context dict to be populated:
        context = {}
        context['request'] = request
        
        queryset = DJIAIndexComposition.objects.all()
        serializer = DJIAIndexSerializer(queryset, many=True, context=context)

        # Extracting the json content from the request body:
        if request.body:
            
            # Loading all data from the request body:
            body_content = json.loads(request.body)

            # Creating or Updating existing model instance via list comprehension:
            django_objs_lst = [
                DJIAIndexComposition.objects.update_or_create(
                    company = json["Company"],

                    defaults = {
                        'exchange' : json["Exchange"],
                        'symbol' : json["Symbol"],
                        'industry' : json["Industry"],
                        'date_added' : json["Date added"],
                        'notes' : json["Notes"],
                        'weighting' : json[list(json)[-1]]
                    }
                    
                    ) for json in body_content]            
                
        return Response(serializer.data)

class SPTSXIndexCompositionViewSet(AbstractModelViewSet):
    """The ViewSets providing the REST API routes for the SPTSXIndexComposition
    database table.
    """
    queryset = SPTSXIndexComposition.objects.all()
    serializer_class = SPTSXIndexSerializer

    def list(self, request):
        """The ViewSet method for processing GET requests to the SPTSX
        Index Database table.
        """
        # Creating a context dict to be populated:
        context = {}
        context["request"] = request

        queryset = SPTSXIndexComposition.objects.all()
        serializer = SPTSXIndexSerializer(queryset, many=True, context=context) 

        return Response(serializer.data)

    def create(self, request):
        """The ViewSet method that contains logic for processing POST requests
        to the SPTSX Index database table.
        """
        # Creating a context dict to be populated:
        context = {}
        context['request'] = request
        
        queryset = SPTSXIndexComposition.objects.all()
        serializer = SPTSXIndexSerializer(queryset, many=True, context=context)

        # Extracting the json content from the request body:
        if request.body:
            
            # Loading all data from the request body:
            body_content = json.loads(request.body)

            # Creating or Updating existing model instance via list comprehension:
            django_objs_lst = [
                SPTSXIndexComposition.objects.update_or_create(
                    symbol = json["Symbol"],

                    defaults = {
                        'company' : json["Company"],
                        'sector' : json["Sector [5]"],
                        'industry' : json["Industry [5]"]
                    }
                    
                    ) for json in body_content]            
                
        return Response(serializer.data)

class FTSE100IndexCompositionViewSet(AbstractModelViewSet):
    """The ViewSets providing the REST API routes for the FTSE100IndexComposition
    database table.
    """
    queryset = FTSE100IndexComposition.objects.all()
    serializer_class = FTSE100IndexSerializer
    
    def list(self, request):
        """The ViewSet method for processing GET requests to the SPTSX
        Index Database table.
        """
        # Creating a context dict to be populated:
        context = {}
        context["request"] = request

        queryset = FTSE100IndexComposition.objects.all()
        serializer = FTSE100IndexSerializer(queryset, many=True, context=context) 

        return Response(serializer.data)

    def create(self, request):
        """The ViewSet method that contains logic for processing POST requests
        to the FTSE100 Index database table.
        """
        # Creating a context dict to be populated:
        context = {}
        context['request'] = request
        
        queryset = FTSE100IndexSerializer.objects.all()
        serializer = FTSE100IndexSerializer(queryset, many=True, context=context)

        # Extracting the json content from the request body:
        if request.body:
            
            # Loading all data from the request body:
            body_content = json.loads(request.body)

            # Creating or Updating existing model instance via list comprehension:
            django_objs_lst = [
                FTSE100IndexComposition.objects.update_or_create(
                    symbol = json["Company"],

                    defaults = {
                        'symbol' : json["EPIC"],
                        'industry' : json["FTSE Industry Classification Benchmark sector[13]"]
                    }
                    
                    ) for json in body_content]            
                
        return Response(serializer.data)

class SMICompositionViewSet(AbstractModelViewSet):
    """The ViewSets providing the REST API routes for the SMIComposition
    database table.
    """
    queryset = SMIComposition.objects.all()
    serializer_class = SMISerializer

    def list(self, request):
        """The ViewSet method for processing GET requests to the SMI
        Index Database table.
        """
        # Creating a context dict to be populated:
        context = {}
        context["request"] = request

        queryset = SMIComposition.objects.all()
        serializer = SMISerializer(queryset, many=True, context=context) 

        return Response(serializer.data)

    def create(self, request):
        """The ViewSet method that contains logic for processing POST requests
        to the SMI Index database table.
        """
        # Creating a context dict to be populated:
        context = {}
        context['request'] = request
        
        queryset = SMIComposition.objects.all()
        serializer = SMISerializer(queryset, many=True, context=context)

        # Extracting the json content from the request body:
        if request.body:
            
            # Loading all data from the request body:
            body_content = json.loads(request.body)

            # Creating or Updating existing model instance via list comprehension:
            django_objs_lst = [
                SMIComposition.objects.update_or_create(
                    symbol = json["Ticker"],

                    defaults = {
                        'rank' : json["Rank"],
                        'company': json["Name"],
                        'industry' : json["Industry"],
                        'canton' : json["Canton"],
                        "weighting" : json["Weighting in\xa0%"]
                    }
                    
                    ) for json in body_content]            
                
        return Response(serializer.data)

class SPICompositionViewSet(AbstractModelViewSet):
    """
    The ViewSets providing the REST API routes for the SPIComposition
    database table.
    """
    queryset = SPIComposition.objects.all()
    serializer_class = SPISerializer

    def list(self, request):
        """The ViewSet method for processing GET requests to the Swiss Performance
        Index Database table.
        """
        # Creating a context dict to be populated:
        context = {}
        context["request"] = request

        queryset = SPIComposition.objects.all()
        serializer = SPISerializer(queryset, many=True, context=context) 

        return Response(serializer.data)

    def create(self, request):
        """The ViewSet method that contains logic for processing POST requests
        to the Swiss Performance Index database table.
        """
        # Creating a context dict to be populated:
        context = {}
        context['request'] = request
        
        queryset = SPIComposition.objects.all()
        serializer = SPISerializer(queryset, many=True, context=context)

        # Extracting the json content from the request body:
        if request.body:
            
            # Loading all data from the request body:
            body_content = json.loads(request.body)

            # Creating or Updating existing model instance via list comprehension:
            django_objs_lst = [
                SPIComposition.objects.update_or_create(
                    symbol = json["Symbol"],

                    defaults = {
                        'company' : json["Company"],
                        'smi_family': json["SMI Family"],
                        'date_added' : json["Listing"],
                        'notes' : json["Remarks"]
                    }
                    
                    ) for json in body_content]            
                
        return Response(serializer.data)

class NASDAQCompositionViewSet(AbstractModelViewSet):
    """
    The ViewSets providing the REST API routes for the NASDAQ
    database table.
    """
    queryset = NASDAQComposition.objects.all()
    serializer_class = NASDAQSerializer

    def list(self, request):
        """The ViewSet method for processing GET requests to the NASDAQ
        Index Database table.
        """
        # Creating a context dict to be populated:
        context = {}
        context["request"] = request

        queryset = NASDAQComposition.objects.all()
        serializer = NASDAQSerializer(queryset, many=True, context=context) 

        return Response(serializer.data)

    def create(self, request):
        """The ViewSet method that contains logic for processing POST requests
        to the NASDAQ Index database table.
        """
        # Creating a context dict to be populated:
        context = {}
        context['request'] = request
        
        queryset = NASDAQComposition.objects.all()
        serializer = NASDAQSerializer(queryset, many=True, context=context)

        # Extracting the json content from the request body:
        if request.body:
            
            # Loading all data from the request body:
            body_content = json.loads(request.body)

            # Creating or Updating existing model instance via list comprehension:
            django_objs_lst = [
                NASDAQComposition.objects.update_or_create(
                    symbol = json["Symbol"],

                    defaults = {
                        'company' : json["Company"],
                        'market_cap': json["Market Cap"],
                        'country' : json["Country"],
                        'ipo_year' : json["IPO Year"],
                        'sector' : json["Sector"],
                        'industry' : json["Industry"]
                    }
                    
                    ) for json in body_content]            
                
        return Response(serializer.data)

class NYSECompositionViewSet(AbstractModelViewSet):
    """
    The ViewSets providing the REST API routes for the NYSE
    database table.
    """
    queryset = NYSEComposition.objects.all()
    serializer_class = NYSESerializer

    def list(self, request):
        """The ViewSet method for processing GET requests to the NYSE
        Index Database table.
        """
        # Creating a context dict to be populated:
        context = {}
        context["request"] = request

        queryset = NYSEComposition.objects.all()
        serializer = NYSESerializer(queryset, many=True, context=context) 

        return Response(serializer.data)

    def create(self, request):
        """The ViewSet method that contains logic for processing POST requests
        to the NYSE Index database table.
        """
        # Creating a context dict to be populated:
        context = {}
        context['request'] = request
        
        queryset = NYSEComposition.objects.all()
        serializer = NYSESerializer(queryset, many=True, context=context)

        # Extracting the json content from the request body:
        if request.body:
            
            # Loading all data from the request body:
            body_content = json.loads(request.body)

            # Creating or Updating existing model instance via list comprehension:
            django_objs_lst = [
                NYSEComposition.objects.update_or_create(
                    symbol = json["Symbol"],

                    defaults = {
                        'company' : json["Company"],
                        'market_cap': json["Market Cap"],
                        'country' : json["Country"],
                        'ipo_year' : json["IPO Year"],
                        'sector' : json["Sector"],
                        'industry' : json["Industry"]
                    }
                    
                    ) for json in body_content]            
                
        return Response(serializer.data)
