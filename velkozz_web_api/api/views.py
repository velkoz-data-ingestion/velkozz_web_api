# Importing Django Methods:
from django.shortcuts import render
from rest_framework import viewsets

# Importing Database Models and Seralizer Objects
from .models import WallStreetBetsPosts, SciencePosts
from .serializers import WallStreetBetsSerializer, SciencePostsSerializer

# Reddit Posts ViewSet:
class WallStreetBetsViewSets(viewsets.ModelViewSet):
    queryset = WallStreetBetsPosts.objects.all().order_by("created_on")
    serializer_class = WallStreetBetsSerializer

class SciencePostsViewSets(viewsets.ModelViewSet):
    queryset = SciencePosts.objects.all().order_by("created_on")
    serializer_class = SciencePostsSerializer