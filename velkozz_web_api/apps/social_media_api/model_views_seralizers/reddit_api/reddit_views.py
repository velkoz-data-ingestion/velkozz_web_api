# Importing Django Methods:
from django.shortcuts import render
from django.contrib.auth.decorators import user_passes_test
from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated


# Importing the custom DjangoModelPermissions and ModelViewSets:
from accounts.permissions import staff_check
from accounts.views import AbstractModelViewSet

# Importing Data Management Packages:
import json
from datetime import date, timedelta
import time
import pandas as pd
import numpy as np

# Importing Database Models and Seralizer Objects
from social_media_api.model_views_seralizers.reddit_api.reddit_models import RedditPosts, RedditDevApps, RedditLogs, RedditPipeline
from .reddit_serializers import RedditPostsSerializer


# Abstract ModelViewSet for Reddit Posts:
class RedditPostViewSet(AbstractModelViewSet):
    """The ViewSet for the Reddit Posts Data model. The ViewSet
    provides all of the CRUD operations for the RedditPosts model and
    connects this model to the REST API. 
    """
    serializer_class = RedditPostsSerializer
    queryset = RedditPosts.objects.all().order_by("created_on")

    def list(self, request):
        """The ViewSet contains the logic for processing GET requests
        to the reddit post database table. It filters posts primarily by
        subreddit.
        """
        # Creating a context dict to be populated:
        context = {}
        context['request'] = request
        
        # Extracting query params from url:
        subreddit = request.GET.get("Subreddit", None)
        start_date = request.GET.get("Start-Date", None)
        end_date = request.GET.get("End-Date", None)
        
        queryset = RedditPosts.objects.all()

        # Conditionals applying logic to queryset based on url params: 

        # Requiring Subreddit Query Param to filter dataset:
        if subreddit is not None:
            queryset = queryset.filter(subreddit=subreddit)

        # Date Time Filtering:
        if start_date is None and end_date is None:
            pass
        else:
            if end_date is None:
                queryset = queryset.filter(created_on__gt=start_date)

            if start_date is None:
                queryset = queryset.filter(created_on__lt=end_date)         

            if start_date and end_date is not None:
                queryset = queryset.filter(created_on__range=(start_date,end_date))

        serializer = RedditPostsSerializer(queryset.order_by("created_on"), many=True, context=context)

        return Response(serializer.data)

@user_passes_test(staff_check)
def reddit_pipeline_dashboard(request):
    """Method renders the dashboard for the status of a reddit pipeline"""
    context = {}

    # Querying the status of the reddit pipeline and its developer app:
    dev_app = RedditDevApps.objects.all().first()
    pipeline = RedditPipeline.objects.all().first()
    reddit_logs = RedditLogs.objects.all()
    reddit_log_errors = reddit_logs.exclude(error_msg=None)
    
    # Creating a 1 week window to filter log queries:
    prev_week = date.today() - timedelta(days=7)
    # Filtering QuerySets:
    reddit_logs = reddit_logs.filter(extracted_on__gt=prev_week).values_list("subreddit", "subreddit_filter", "extracted_on", "num_posts", "status_code", "error_msg")
    
    # Unpacking the reddit logs into a plottable format:
    
    # Converting Reddit Log values into dataframe:
    reddit_log_cols = ["subreddit", "subreddit_filter", "extracted_on", "num_posts", "status_code", "error_msg"]
    reddit_logs_df = pd.DataFrame.from_records(reddit_logs, columns=reddit_log_cols, index="extracted_on")

    # Adding counter variable for resampling:
    reddit_logs_df["_counter"] = 1 

    # Populating the context:
    context["DevApp"] = dev_app
    context["pipeline"] = pipeline
    
    # Logic to not resample if index is broken (eg: There is no data so index is an empty list):
    if len(reddit_logs_df) == 0:
        return render(request, "social_media_api/reddit_pipeline_dash.html", context=context)
    else:
        # Resampling the dataframe into all plottable datasets:
        daily_resample_rate = reddit_logs_df["_counter"].squeeze().resample("D").sum()
        num_posts_seconds_resample = reddit_logs_df["num_posts"].squeeze().resample("H").sum()

        # Resampling dataframe for the number of posts extracted based on fliters:
        top_filter_resample = reddit_logs_df[reddit_logs_df["subreddit_filter"] == "top"]["_counter"].squeeze().resample('D').sum()
        hot_filter_resample = reddit_logs_df[reddit_logs_df["subreddit_filter"] == "hot"]["_counter"].squeeze().resample('D').sum()

        # Resample for status codes 
        status_code_200_resample = reddit_logs_df[reddit_logs_df["status_code"] == 200]["_counter"].squeeze().resample('D').sum()
        status_code_400_resample = reddit_logs_df[reddit_logs_df["status_code"] == 400]["_counter"].squeeze().resample('D').sum()

        # Adding to Context:
        context["Daily_Logs"] = {
            "Data": daily_resample_rate.values.tolist(),
            "Index": daily_resample_rate.index.tolist()
        }
        context["Num_Posts_Seconds"] = {
            "Data" : num_posts_seconds_resample.values.tolist(),
            "Index": num_posts_seconds_resample.index.tolist()
        }
        context["Top_Logs"] = {
            "Data": top_filter_resample.values.tolist(),
            "Index": top_filter_resample.index.tolist()
        }
        context["Hot_Logs"] = {
            "Data": hot_filter_resample.values.tolist(),
            "Index": hot_filter_resample.index.tolist()
        }
        context["Status_Code_200_Logs"] = {
            "Data": status_code_200_resample.values.tolist(),
            "Index": status_code_200_resample.index.tolist()
        }
        context["Status_Code_400_Logs"] = {
            "Data": status_code_400_resample.values.tolist(),
            "Index": status_code_400_resample.index.tolist()
        }
        context["Errors"] = reddit_log_errors

        return render(request, "social_media_api/reddit_pipeline_dash.html", context=context)