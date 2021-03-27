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
from social_media_api.models.reddit.reddit_models import WallStreetBetsPosts, SciencePosts, WorldNewsPosts
from .reddit_serializers import WallStreetBetsSerializer, SciencePostsSerializer, RedditPostsSerializer


# Abstract ModelViewSet for Reddit Posts:
class RedditPostViewSet(AbstractModelViewSet):
    """
    """
    init_model = None
    queryset = None
    
    current_seralizer = RedditPostsSerializer
    current_seralizer.Meta.model = init_model    
    
    serializer_class = current_seralizer

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
        
        queryset = self.init_model.objects.all()

        # Conditionals applying logic to queryset based on url params: 
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

        serializer = self.serializer_class(queryset.order_by("created_on"), many=True, context=context)

        return Response(serializer.data)
    
    def create(self, request):
        """
        """
        # Creating a context dict to be populated:
        context = {}
        context['request'] = request
        
        queryset = self.init_model.objects.all().order_by("created_on")

        # If Requests Body contains POST data:
        if request.body:
            posts = json.loads(request.body)
        else:
            posts = {} # Empty Json if no body content.

        # Creating a list of WallStreetBetsPosts object from Json data via list comprehension:
        posts_objects = [
            self.init_model(
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
                permalink = post["link"],
                author = post["author"],
                author_created = post["acc_created_on"],
                comment_karma = post["comment_karma"]) 

            for post in posts 
        ]
        print(posts_objects)
        
        # Performing a bulk insert for all posts recieved by the POST request:
        self.init_model.objects.bulk_create(posts_objects)
        
        # Seralizing the objects that had been creatd:
        serializer = self.serializer_class(posts_objects, many=True)
        
        # TODO: Fix Serializer. Seralizer is not seralizing data from post list. Regestering as NoneType
        # TODO: Seralizer Issue, may have to bail on dynamically changing seralizer.
        return Response(serializer.data)


# World News Posts:
class WorldNewsViewSet(RedditPostViewSet):
    init_model = WorldNewsPosts
    queryset = init_model.objects.all()

    class Meta:
        verbose_name_plural = "WorldNews Posts"


# Reddit Posts ViewSets:
class WallStreetBetsViewSet(AbstractModelViewSet):
    """The ViewSet that provides REST API routes for the subreddit WallStreetBets
    post database table.
    """
    serializer_class = WallStreetBetsSerializer
    queryset = WallStreetBetsPosts.objects.none()
    
    def list(self, request):
        """The ViewSet method overwritten that contains the
        logic for processing GET requests from the r/wallstreetbets post
        database table.   
        """
        # Creating a context dict to be populated:
        context = {}
        context['request'] = request
        
        # Extracting query params from url:
        start_date = request.GET.get("Start-Date", None)
        end_date = request.GET.get("End-Date", None)
        
        queryset = WallStreetBetsPosts.objects.all()

        # Conditionals applying logic to queryset based on url params: 
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

        serializer = WallStreetBetsSerializer(queryset.order_by("created_on"), many=True, context=context)

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
        else:
            wsb_posts = {} # Empty Json if no body content.

        # Creating a list of WallStreetBetsPosts object from Json data via list comprehension:
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
                permalink = post["link"],
                author = post["author"],
                author_created = post["acc_created_on"],
                comment_karma = post["comment_karma"]) 

            for post in wsb_posts 
        ]

        # Performing a bulk insert for all posts recieved by the POST request:
        WallStreetBetsPosts.objects.bulk_create(wsb_posts_objects)
        
        return Response(serializer.data)

    class Meta:
        verbose_name_plural = "WallStreetBets Post"

class SciencePostsViewSet(AbstractModelViewSet):
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
                permalink = post["link"],
                author = post["author"],
                author_created = post["acc_created_on"],
                comment_karma = post["comment_karma"]) 

            for post in science_posts 
        ]

        # Performing a bulk insert for all posts recieved by the POST request:
        SciencePosts.objects.bulk_create(science_posts_objects)
        
        return Response(serializer.data)