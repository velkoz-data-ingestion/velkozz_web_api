# Importing Django Methods:
from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

# Importing the custom DjangoModelPermissions Module:
from accounts.permissions import APIModelPermissions

# Importing Data Management Packages:
import json

# Importing Database Models and Seralizer Objects
from social_media_api.models.reddit.reddit_models import WallStreetBetsPosts, SciencePosts
from .reddit_serializers import WallStreetBetsSerializer, SciencePostsSerializer

# Reddit Posts ViewSets:
class WallStreetBetsViewSet(viewsets.ModelViewSet):
    """The ViewSet that provides REST API routes for the subreddit WallStreetBets
    post database table.
    """
    serializer_class = WallStreetBetsSerializer
    queryset = WallStreetBetsPosts.objects.none()
    permission_classes = [IsAuthenticated, APIModelPermissions]    

    def list(self, request):
        """The ViewSet method overwritten that contains the
        logic for processing GET requests from the r/wallstreetbets post
        database table.   
        """
        # Creating a context dict to be populated:
        context = {}
        context['request'] = request
        
        # Querying all elements from the database:
        queryset = WallStreetBetsPosts.objects.all().order_by("created_on")
        serializer = WallStreetBetsSerializer(queryset, many=True, context=context)

        return Response(serializer.data)
    
    def create(self, request):
        """The ViewSet method overwritten that contains the
        logic for processing POST requests to the r/wallstreetbets posts
        database table. 
        """
        # Creating a context dict to be populated:
        context = {}
        context['request'] = request
        
        queryset = WallStreetBetsPosts.objects.all().order_by("created_on")
        serializer = WallStreetBetsSerializer(queryset, many=True, context=context)

        # If Requests Body contains POST data:
        if request.body:
            wsb_posts = json.loads(request.body)

        # Creating a list of SciencePosts object from Json data via list comprehension:
        wsb_posts_objects = [
            WallStreetBetsPosts(
                id = post["id"],
                title = post["title"],
                content = post["content"],
                upvote_ratio = post["upvote_ratio"],
                score = post["score"],
                num_comments= post["num_comments"],
                created_on = post["created_on"],
                stickied= post["stickied"],
                over_18 = post["over_18"],
                spoiler = post["spoiler"],
                author_is_gold = post["author_gold"],
                author_mod = post["mod_status"],
                author_has_verified_email = post["verified_email_status"],
                permalink = post["permalink"],
                author = post["author"],
                author_created = post["acc_created_on"],
                comment_karma = post["comment_karma"]) 

            for post in wsb_posts 
        ]

        # Performing a bulk insert for all posts recieved by the POST request:
        SciencePosts.objects.bulk_create(wsb_posts_objects)
        
        return Response(serializer.data)

class SciencePostsViewSet(viewsets.ModelViewSet):
    """The ViewSet that provides REST API routes for the subreddit WallStreetBets
    post database table.
    """
    queryset = SciencePosts.objects.all().order_by("created_on")
    serializer_class = SciencePostsSerializer

    def list(self, request):
        """The ViewSet method overwritten that contains the
        logic for processing GET requests from the r/science post
        database table.  
        """
        # Creating a context dict to be populated:
        context = {}
        context['request'] = request
        
        # Querying all elements from the database:
        queryset = SciencePosts.objects.all().order_by("created_on")
        serializer = SciencePostsSerializer(queryset, many=True, context=context)

        return Response(serializer.data)

    def create(self, request):
        """The ViewSet method overwritten that contains the
        logic for processing POST requests to the r/science posts
        database table. 
        """
        # Creating a context dict to be populated:
        context = {}
        context['request'] = request
        
        queryset = SciencePosts.objects.all().order_by("created_on")
        serializer = SciencePostsSerializer(queryset, many=True, context=context)

        # If Requests Body contains POST data:
        if request.body:
            science_posts = json.loads(request.body)

        # Creating a list of SciencePosts object from Json data via list comprehension:
        science_posts_objects = [
            SciencePosts(
                id = post["id"],
                title = post["title"],
                content = post["content"],
                upvote_ratio = post["upvote_ratio"],
                score = post["score"],
                num_comments= post["num_comments"],
                created_on = post["created_on"],
                stickied= post["stickied"],
                over_18 = post["over_18"],
                spoiler = post["spoiler"],
                author_is_gold = post["author_gold"],
                author_mod = post["mod_status"],
                author_has_verified_email = post["verified_email_status"],
                permalink = post["permalink"],
                author = post["author"],
                author_created = post["acc_created_on"],
                comment_karma = post["comment_karma"]) 

            for post in science_posts 
        ]

        # Performing a bulk insert for all posts recieved by the POST request:
        SciencePosts.objects.bulk_create(science_posts_objects)
        
        return Response(serializer.data)