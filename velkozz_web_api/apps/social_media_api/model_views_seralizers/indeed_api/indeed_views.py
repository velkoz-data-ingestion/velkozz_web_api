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
from social_media_api.models.indeed import indeed_models
from .indeed_serializers import *

# VeiwSet for the Indeed Job Postings:
class IndeedJobPostsViewSets(AbstractModelViewSet):
    """The ViewSet for the Indeed Job Posts data model. The ViewSet
    provides all of the CRUD operations for the IndeedJobPosts model and
    connects this model to the REST API. 
    """
    serializer_class = IndeedJobsPostsSerializer
    queryset = indeed_models.IndeedJobPosts.objects.all().order_by("date_posted")

    def list(self, request):
        """The ViewSet method overwritten that contains the
        logic for processing GET requests from the generic post
        database table.   
        """
        # Creating a context dict to be populated:
        context = {}
        context['request'] = request

        # Extracting query params from url:
        start_date = request.GET.get("Start-Date", None)
        end_date = request.GET.get("End-Date", None)
        location_query = request.GET.get("location", None)
        
        # Querying and seralizing the database for Indeed Posts:
        queryset = indeed_models.IndeedJobPosts.objects.all()

        # Conditionals applying logic to queryset based on url params: 
        # Date Time Filtering:
        if start_date is None and end_date is None:
            pass
        else:
            if end_date is None:
                queryset = queryset.filter(date_posted__gt=start_date)

            if start_date is None:
                queryset = queryset.filter(date_posted__lt=end_date)         

            if start_date and end_date is not None:
                queryset = queryset.filter(date_posted__range=(start_date,end_date))

        # Location Filtering:
        if location_query is not None:
            queryset= queryset.filter(location__contains=location_query)
        
        serializer = IndeedJobsPostsSerializer(queryset, many=True, context=context)
        
        return Response(serializer.data)

    def create(self, request):
        """The ViewSet method that processes POST requests made to the
        IndeedJobPostings API.


        The method de-seralizes the JSON payload and uses the bulk create-or-update
        django method to write ticker frequency counts to the database.
        """
        # Extracting payload from request body:
        if request.body:
            body_content = json.loads(request.body)

            # Creating or updating the indeed job model based on primary key:
            job_listings = [
                indeed_models.IndeedJobPosts.objects.update_or_create(
                    id=listing["id"], 

                    defaults = {
                        "title":listing["title"],    
                        "company":listing["company"],
                        "location":listing["location"],
                        "summary":listing["summary"],
                        "date_posted":listing['date_posted']
                    }
                    
                ) for listing in body_content
            ]

        return Response(body_content)