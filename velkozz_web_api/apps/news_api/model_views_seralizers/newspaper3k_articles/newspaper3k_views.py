# Importing News Article models and serilaziers: 
from accounts.views import AbstractModelViewSet
from .newspaper3k_models import NewsArticles
from .newspaper3k_seralizers import NewsArticlesSeralizer

# Importing DRF ViewSet packages:
from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import Permission
from django.http import HttpResponseNotFound 

# Importing 3rd Party Packages:
import pandas as pd 
import csv
import os
import json

class NewsArticlesViewSet(AbstractModelViewSet):
    """The ViewSet providing the REST API routes for the News Articles
    django model. It provides all CRUD operations for the model.
    """
    queryset = NewsArticles.objects.all()
    serializer_class = NewsArticlesSeralizer

    def list(self, request):
        """Overwrites the default handler for GET request made to the
        REST API.
        """ 
        # Creating the context to be populated:
        context = {}
        context["request"] = request

        # TODO: Extract the query params from the url.
        start_date = request.GET.get("Start-Date", None)
        end_date = request.GET.get("End-Date", None)
        source = request.GET.get("Source", None)
        authors = request.GET.get("Authors", None)

        # Creating initial large queryset to be filtered:
        queryset = NewsArticles.objects.all()

        # TODO: QuerySet Filtering:
        if start_date is None and end_date is None:
            pass
        else:
            if end_date is None:
                queryset = queryset.filter(published_date__gt=start_date)

            if start_date is None:
                queryset = queryset.filter(published_date__lt=end_date)         

            if start_date and end_date is not None:
                queryset = queryset.filter(published_date__range=(start_date, end_date))

        if source is not None:
            queryset = queryset.filter(source=source)

        # TODO: Author names filter:

        # Seralizing the queryset into JSON response:
        serializer = NewsArticlesSeralizer(queryset, many=True, context=context)

        return Response(serializer.data, status=status.HTTP_202_ACCEPTED)

    def create(self, request):
        """Overwrites the default handler for POST requets made to the
        API.
        
        The method de-seralizes the JSON payload and uses the bulk create-or-update
        django method to write data to the database.
        """
        # Extracting payload from request body:
        if request.body:
            body_content = json.loads(request.body)
            
            # Counter for the data being written to the database:
            written = 0
            errors = 0
            for article in body_content:
                # Writing data to the database via the serializer:
                serializer = NewsArticlesSeralizer(data=article)
                
                # If the serializer has validated the data, write the data to the database via the ORM:
                if serializer.is_valid():
                    
                    obj, created = NewsArticles.objects.update_or_create(
                            title = serializer.validated_data["title"],
                            
                            defaults = {
                                
                                "published_date":serializer.validated_data["published_date"],
                                "authors":serializer.validated_data["authors"],
                                "article_text":serializer.validated_data["article_text"],
                                "meta_keywords":serializer.validated_data["meta_keywords"],
                                "nlp_keywords":serializer.validated_data["nlp_keywords"],
                                "article_url":serializer.validated_data["article_url"],
                                "source":serializer.validated_data["source"],
                                "timestamp":serializer.validated_data["timestamp"],
                            }
                    )

                    written = written + 1    
                
                else:
                    errors = errors + 1
                    print(serializer.errors)

            # Building Body Content:
            example_source = body_content[0]["source"]
            response_content = f"POST Request made to news_api with {len(body_content)} {example_source} articles. Success: {written} Failure: {errors} \n Example: {body_content[0]}"

            # Building the response after writing data to the database:
            return Response(response_content, status=status.HTTP_201_CREATED)    
                  
        return HttpResponseNotFound("POST Response Error")
