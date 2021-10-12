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

# Importing Database Models and Seralizer Objects
from social_media_api.models.reddit.reddit_models import RedditPosts
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
    
    def create(self, request):
        """The method that processes the POST requests made to the REST API and
        creates the django model objects necessary to write subreddit post data to the database. 
        """
        # Creating a context dict to be populated:
        context = {}
        context['request'] = request
        
        queryset = RedditPosts.objects.all().order_by("created_on")

        # If Requests Body contains POST data:
        if request.body:
            posts = json.loads(request.body)
        else:
            posts = {} # Empty Json if no body content.

        # Performing a bulk insert for all posts recieved by the POST request:
        posts_objects = [
            RedditPosts.objects.update_or_create(
                id = post["id"],
                defaults= {
                "id":post["id"],
                "subreddit": post["subreddit"],
                "title":post["title"],
                "content":post["content"],
                "upvote_ratio":post["upvote_ratio"],
                "score":post["score"],
                "num_comments":post["num_comments"],
                "created_on":post["created_on"],
                "stickied":post["stickied"],
                "over_18":post["over_18"],
                "spoiler":post["spoiler"],
                "author_is_gold":post["author_gold"],
                "author_mod":post["mod_status"],
                "author_has_verified_email":post["verified_email_status"],
                "permalink":post["link"],
                "author":post["author"],
                "author_created":post["acc_created_on"],
                "comment_karma":post["comment_karma"]}                
            ) for post in posts
        ]
        
        # Seralizing the objects that had been creatd:
        posts_objects = [post[0] for post in posts_objects]
        serializer = RedditPostsSerializer(posts_objects, many=True, context=context)
        
        return Response(serializer.data)


