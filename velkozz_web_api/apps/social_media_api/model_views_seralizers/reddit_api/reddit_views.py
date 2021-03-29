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
from social_media_api.models.reddit import reddit_models
from .reddit_serializers import *

# Abstract ModelViewSet for Reddit Posts:
class RedditPostViewSet(AbstractModelViewSet):
    """Abstract class for the ModelViewSet for Subreddit database
    models. 
    """
    serializer_class = None
    init_model = None
    queryset = None

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
        serializer = self.serializer_class(posts_objects, many=True, context=context)
        
        return Response(serializer.data)


# Subreddit Specific ViewSets:
class WallStreetBetsViewSet(RedditPostViewSet):
    serializer_class = WallStreetBetsPostsSerializer
    init_model = serializer_class.Meta.model
    queryset = init_model.objects.all().order_by("created_on")

class SciencePostsViewSet(RedditPostViewSet):
    serializer_class = SciencePostsSerializer
    init_model = serializer_class.Meta.model
    queryset = init_model.objects.all().order_by("created_on")

class WorldNewsPostsViewSet(RedditPostViewSet):
    serializer_class = WorldNewsPostsSerializer
    init_model = serializer_class.Meta.model
    queryset = init_model.objects.all().order_by("created_on")

class NewsPostsViewSet(RedditPostViewSet):
    serializer_class = NewsPostsSerializer
    init_model = serializer_class.Meta.model
    queryset = init_model.objects.all().order_by("created_on")

class EnergyPostsViewSet(RedditPostViewSet):
    serializer_class = EnergyPostsSerializer
    init_model = serializer_class.Meta.model
    queryset = init_model.objects.all().order_by("created_on")

class EconomicsPostsViewSet(RedditPostViewSet):
    serializer_class = EconomicsPostsSerializer
    init_model = serializer_class.Meta.model
    queryset = init_model.objects.all().order_by("created_on")

class PoliticsPostsViewSet(RedditPostViewSet):
    serializer_class = PoliticsPostsSerializer
    init_model = serializer_class.Meta.model
    queryset = init_model.objects.all().order_by("created_on")

class CanadaPostsViewSet(RedditPostViewSet):
    serializer_class = CanadaPostsSerializer
    init_model = serializer_class.Meta.model
    queryset = init_model.objects.all().order_by("created_on")

class UKPoliticsPostsViewSet(RedditPostViewSet):
    serializer_class = UKPoliticsPostsSerializer
    init_model = serializer_class.Meta.model
    queryset = init_model.objects.all().order_by("created_on")

class PalestinePostsViewSet(RedditPostViewSet):
    serializer_class = PalestinePostsSerializer
    init_model = serializer_class.Meta.model
    queryset = init_model.objects.all().order_by("created_on")

class MiddleEastNewsPostsViewSet(RedditPostViewSet):
    serializer_class = MiddleEastNewsPostsSerializer
    init_model = serializer_class.Meta.model
    queryset = init_model.objects.all().order_by("created_on")

class IsraelPostsViewSet(RedditPostViewSet):
    serializer_class = IsraelPostsSerializer
    init_model = serializer_class.Meta.model
    queryset = init_model.objects.all().order_by("created_on")

class PakistanPostsViewSet(RedditPostViewSet):
    serializer_class = PakistanPostsSerializer
    init_model = serializer_class.Meta.model
    queryset = init_model.objects.all().order_by("created_on")

class IndiaPostsViewSet(RedditPostViewSet):
    serializer_class = IndiaPostsSerializer
    init_model = serializer_class.Meta.model
    queryset = init_model.objects.all().order_by("created_on")

class LiberalPostsViewSet(RedditPostViewSet):
    serializer_class = LiberalPostsSerializer
    init_model = serializer_class.Meta.model
    queryset = init_model.objects.all().order_by("created_on")

class ConservativePostsViewSet(RedditPostViewSet):
    serializer_class = ConservativePostsSerializer
    init_model = serializer_class.Meta.model
    queryset = init_model.objects.all().order_by("created_on")

class SocialismPostsViewSet(RedditPostViewSet):
    serializer_class = SocialismPostsSerializer
    init_model = serializer_class.Meta.model
    queryset = init_model.objects.all().order_by("created_on")

class ProgressivePostsViewSet(RedditPostViewSet):
    serializer_class = ProgressivePostsSerializer
    init_model = serializer_class.Meta.model
    queryset = init_model.objects.all().order_by("created_on")

class DemocratsPostsViewSet(RedditPostViewSet):
    serializer_class = DemocratsPostsSerializer
    init_model = serializer_class.Meta.model
    queryset = init_model.objects.all().order_by("created_on")

class LiberalPostsViewSet(RedditPostViewSet):
    serializer_class = LiberalPostsSerializer
    init_model = serializer_class.Meta.model
    queryset = init_model.objects.all().order_by("created_on")

class TechnologyPostsViewSet(RedditPostViewSet):
    serializer_class = TechnologyPostsSerializer
    init_model = serializer_class.Meta.model
    queryset = init_model.objects.all().order_by("created_on")

class RealTechPostsViewSet(RedditPostViewSet):
    serializer_class = RealTechPostsSerializer
    init_model = serializer_class.Meta.model
    queryset = init_model.objects.all().order_by("created_on")

class TechPostsViewSet(RedditPostViewSet):
    serializer_class = TechPostsSerializer
    init_model = serializer_class.Meta.model
    queryset = init_model.objects.all().order_by("created_on")

class NeutralPoliticsViewSet(RedditPostViewSet):
    serializer_class = NeutralPoliticsPostsSerializer
    init_model = serializer_class.Meta.model
    queryset = init_model.objects.all().order_by("created_on")

class ChinaPostsViewSet(RedditPostViewSet):
    serializer_class = ChinaPostsSerializer
    init_model = serializer_class.Meta.model
    queryset = init_model.objects.all().order_by("created_on")

class TaiwanPostsViewSet(RedditPostViewSet):
    serializer_class = TaiwanPostsSerializer
    init_model = serializer_class.Meta.model
    queryset = init_model.objects.all().order_by("created_on")

class JapanPostsViewSet(RedditPostViewSet):
    serializer_class = JapanPostsSerializer
    init_model = serializer_class.Meta.model
    queryset = init_model.objects.all().order_by("created_on")

class KoreaPostsViewSet(RedditPostViewSet):
    serializer_class = KoreaPostsSerializer
    init_model = serializer_class.Meta.model
    queryset = init_model.objects.all().order_by("created_on")

class SingaporePostsViewSet(RedditPostViewSet):
    serializer_class = SingaporePostsSerializer
    init_model = serializer_class.Meta.model
    queryset = init_model.objects.all().order_by("created_on")

class MalaysiaPostsViewSet(RedditPostViewSet):
    serializer_class = MalaysiaPostsSerializer
    init_model = serializer_class.Meta.model
    queryset = init_model.objects.all().order_by("created_on")

class ThailandPostsViewSet(RedditPostViewSet):
    serializer_class = ThailandPostsSerializer
    init_model = serializer_class.Meta.model
    queryset = init_model.objects.all().order_by("created_on")

class NorthKoreaPostsViewSet(RedditPostViewSet):
    serializer_class = NorthKoreaPostsSerializer
    init_model = serializer_class.Meta.model
    queryset = init_model.objects.all().order_by("created_on")

class NorthKoreaNewsPostsViewSet(RedditPostViewSet):
    serializer_class = NorthKoreaNewsPostsSerializer
    init_model = serializer_class.Meta.model
    queryset = init_model.objects.all().order_by("created_on")

class ConflictNewsPostsViewSet(RedditPostViewSet):
    serializer_class = ConflictNewsPostsSerializer
    init_model = serializer_class.Meta.model
    queryset = init_model.objects.all().order_by("created_on")

class HongKongPostsViewSet(RedditPostViewSet):
    serializer_class = HongKongPostsSerializer
    init_model = serializer_class.Meta.model
    queryset = init_model.objects.all().order_by("created_on")

class SpacePostsViewSet(RedditPostViewSet):
    serializer_class = SpacePostsSerializer
    init_model = serializer_class.Meta.model
    queryset = init_model.objects.all().order_by("created_on")

class CryptoCurrencyPostsViewSet(RedditPostViewSet):
    serializer_class = CryptoCurrencyPostsSerializer
    init_model = serializer_class.Meta.model
    queryset = init_model.objects.all().order_by("created_on")