# Importing Django Methods:
from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response

# Importing Data Management Packages:
import json

# Importing the Market Index Seralizers and Database Models:
from .market_indicies_models import *
from .market_indicies_serializers import * 

# Market Indicies ModelViewSet
class SPYIndexCompositionViewSet(viewsets.ModelViewSet):
    """The ViewSets providing the REST API routes for the SPYIndexComposition
    database table.
    """
    queryset = SPYIndexComposition.objects.all()
    serializer_class = SPYIndexSerializer

class DJIAIndexCompositionViewSet(viewsets.ModelViewSet):
    """The ViewSets providing the REST API routes for the DJIAIndexComposition
    database table.
    """
    queryset = DJIAIndexComposition.objects.all()
    serializer_class = DJIAIndexSerializer

class SPTSXIndexCompositionViewSet(viewsets.ModelViewSet):
    """The ViewSets providing the REST API routes for the SPTSXIndexComposition
    database table.
    """
    queryset = SPTSXIndexComposition.objects.all()
    serializer_class = SPTSXIndexSerializer

class FTSE100IndexCompositionViewSet(viewsets.ModelViewSet):
    """The ViewSets providing the REST API routes for the FTSE100IndexComposition
    database table.
    """
    queryset = FTSE100IndexComposition.objects.all()
    serializer_class = FTSE100IndexSerializer
    
class SMICompositionViewSet(viewsets.ModelViewSet):
    """The ViewSets providing the REST API routes for the SMIComposition
    database table.
    """
    queryset = SMIComposition.objects.all()
    serializer_class = SMISerializer

class SPICompositionViewSet(viewsets.ModelViewSet):
    """
    The ViewSets providing the REST API routes for the SPIComposition
    database table.
    """
    queryset = SPIComposition.objects.all()
    serializer_class = SPISerializer