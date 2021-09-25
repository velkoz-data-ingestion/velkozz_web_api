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

# Importing Database Models and Seralizer Objects: 
from social_media_api.models.youtube import youtube_models
from .youtube_serializers import *

# Daily Youtube Channel Statistics ViewSet:
class DailyYoutubeChannelStatsViewSet(AbstractModelViewSet):
    """The ViewSet for the Daily Youtube Channel Statistics data model. The ViewSet
    provides all of the CRUD operations for the DailyYoutubeChannelStats model and
    connects this model to the REST API. 
    """
    serializer_class = DailyYoutubeChannelStatsSerializer
    queryset = youtube_models.DailyYoutubeChannelStats.objects.all().order_by("date_extracted")

    def list(self, request):
        """The ViewSet method overwritten that contains the
        logic for processing GET requests from the generic post
        database table.   
        """
        # Creating a context dict to be populated: 
        context = {}
        context["request"] = request
        
        # Extracting Query Params from the url:
        start_date = request.GET.get("Start-Date", None)
        end_date = request.GET.get("End-Date", None)
        channel_name = request.GET.get("Channel-Name", None)
        channel_id = request.GET.get("Channel-ID", None)

        # Querying and seralizing the database for Youtube Channel Posts:
        queryset = youtube_models.DailyYoutubeChannelStats.objects.all()

        # Filtering the queryset based on the url query params:
        # Date Time Filtering:
        if start_date is None and end_date is None:
            pass
        else:
            if end_date is None:
                queryset = queryset.filter(date_extracted__gt=start_date)

            if start_date is None:
                queryset = queryset.filter(date_extracted__lt=end_date)         

            if start_date and end_date is not None:
                queryset = queryset.filter(date_extracted__range=(start_date, end_date))

        # Channel Name Filtering:
        if channel_name is not None:
            queryset = queryset.filter(channel_name=channel_name)

        # Channel ID Filtering:
        if channel_id is not None:
            queryset = queryset.filter(channel_id=channel_id)

        serializer = DailyYoutubeChannelStatsSerializer(queryset, many=True, context=context)

        if len(queryset) == 0:
            return Response([{"Response": "No Data Found for Youtube Channel Stats, QuerySet Empty"}])

        return Response(serializer.data)

    def create(self, request):
        """The ViewSet method that processes POST requests made to the
        DailyYoutubeChannelStats API.


        The method de-seralizes the JSON payload and uses the bulk create-or-update
        django method to write to the Youtube Channel Database.
        """
        # Creating a context dict to be populated:
        context = {}
        context["request"] = request

        # Attempting to extract payload from the request body:
        if request.body:
            channel_data = json.loads(request.body)
        else:
            data = {} # Empty Json if no body content

        # Creating or updating the Youtube Channel model:
        youtube_channel_data = [
            youtube_models.DailyYoutubeChannelStats.objects.update_or_create(
                channel_id=data["channel_id"],
                channel_name=data["channel_name"], 
                total_views=data["viewCount"],
                total_subscribers=data["subscriberCount"],
                total_videos=data["videoCount"],
                ) for data in channel_data
        ]

        # Seralizing the objects that had been created:
        youtube_channel_data = [channel_data[0] for channel_data in youtube_channel_data]
        serializer = DailyYoutubeChannelStatsSerializer(youtube_channel_data, many=True, context=context)

        return Response(serializer.data)

        

