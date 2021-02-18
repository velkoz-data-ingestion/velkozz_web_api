# Importing Data management packages: 
import json
from collections import OrderedDict
from datetime import datetime
from dateutil.parser import parse

# Importing Testing Framework:
from rest_framework import status
from django.test import TestCase, Client
from django.urls import reverse
from rest_framework.test import APIRequestFactory, force_authenticate
from rest_framework.request import Request
from django.forms.models import model_to_dict

# Importing a base RedditModel TestCase:
from .base_social_media_testcases import AbstractRedditModelTestCase

# Importing Account Data Models; 
from accounts.models import CustomUser

# Importing Subreddit Models and Seralizers:
from ..models.reddit.reddit_models import WallStreetBetsPosts, SciencePosts
from ..model_views_seralizers.reddit_api.reddit_serializers import WallStreetBetsSerializer, SciencePostsSerializer

# Importing the Views:
from ..model_views_seralizers.reddit_api.reddit_views import WallStreetBetsViewSet, SciencePostsViewSet

class WallStreetBetsPostsTest(AbstractRedditModelTestCase, TestCase):
    """
    Object performs GET and POST requests to the Reddit WallStreetBetsPosts API
    to ensure correct data ingestion and reading.
    """
    def setUp(self):

        # Declaring Instance Config Parameter:
        self.RedditModel = WallStreetBetsPosts
        self.ModelViewSet = WallStreetBetsViewSet
        self.api_url = "/social_media_api/reddit/rwallstreetbets/"

        # Creating WallStreetBets model objects for testing:
        self.RedditModel.objects.bulk_create([
            self.RedditModel(
            id = "test45",
            title = "This is a Test Title",
            content = "This is some Test Content",
            upvote_ratio = 0.77,
            score = 2625,
            num_comments = 580,
            created_on = "2021-02-09T02:08:58Z",
            stickied = False,
            over_18 = False,
            spoiler = False,
            author_is_gold = False,
            author_mod = False,
            author_has_verified_email = True,
            permalink = "/r/wallstreetbets/comments/lfs22f/why_ill_never_stop_buying_gme_and_why_you/",
            author = "A_test_author",
            author_created = "2019-08-20T02:31:19Z",
            comment_karma = 2504),
            self.RedditModel(
            id = "test67",
            title = "This is a Test Title",
            content = "This is some Test Content",
            upvote_ratio = 0.77,
            score = 2625,
            num_comments = 580,
            created_on = "2021-02-09T02:08:58Z",
            stickied = True,
            over_18 = True,
            spoiler = False,
            author_is_gold = False,
            author_mod = False,
            author_has_verified_email = True,
            permalink = "/r/wallstreetbets/comments/lfs22f/why_ill_never_stop_buying_gme_and_why_you/",
            author = "A_test_author",
            author_created = "2019-08-20T02:31:19Z",
            comment_karma = 2504),
            self.RedditModel(
            id = "qwerty",
            title = "This is a Test Title",
            content = "This is some Test Content",
            upvote_ratio = 0.77,
            score = 2625,
            num_comments = 580,
            created_on = "2021-02-09T02:08:58Z",
            stickied = False,
            over_18 = False,
            spoiler = False,
            author_is_gold = False,
            author_mod = False,
            author_has_verified_email = True,
            permalink = "/r/wallstreetbets/comments/lfs22f/why_ill_never_stop_buying_gme_and_why_you/",
            author = "A_test_author",
            author_created = "2019-08-20T02:31:19Z",
            comment_karma = 2504),
            self.RedditModel(
            id = "asdfxz",
            title = "This is a Test Title",
            content = "This is some Test Content",
            upvote_ratio = 0.77,
            score = 2625,
            num_comments = 580,
            created_on = "2021-02-09T02:08:58Z",
            stickied = False,
            over_18 = False,
            spoiler = False,
            author_is_gold = False,
            author_mod = False,
            author_has_verified_email = True,
            permalink = "/r/wallstreetbets/comments/lfs22f/why_ill_never_stop_buying_gme_and_why_you/",
            author = "A_test_author",
            author_created = "2019-08-20T02:31:19Z",
            comment_karma = 2504)
        ])

class SciencePostsTest(AbstractRedditModelTestCase, TestCase):
    """
    Object to perform all the GET and POST requests to the Reddit SciencePosts
    API to ensure correct data ingestion and reading.
    """
    def setUp(self):

        # Declaring Instance Config Parameter:
        self.RedditModel = SciencePosts
        self.ModelViewSet = SciencePostsViewSet
        self.api_url = "/social_media_api/reddit/rscience/"

        # Writing test data to be database:
        self.RedditModel.objects.bulk_create([
            self.RedditModel(
            id = "test45",
            title = "This is a Test Title",
            content = "This is some Test Content",
            upvote_ratio = 0.77,
            score = 2625,
            num_comments = 580,
            created_on = "2021-02-09T02:08:58Z",
            stickied = False,
            over_18 = False,
            spoiler = False,
            author_is_gold = False,
            author_mod = False,
            author_has_verified_email = True,
            permalink = "/r/wallstreetbets/comments/lfs22f/why_ill_never_stop_buying_gme_and_why_you/",
            author = "A_test_author",
            author_created = "2019-08-20T02:31:19Z",
            comment_karma = 2504),
            self.RedditModel(
            id = "test67",
            title = "This is a Test Title",
            content = "This is some Test Content",
            upvote_ratio = 0.77,
            score = 2625,
            num_comments = 580,
            created_on = "2021-02-09T02:08:58Z",
            stickied = True,
            over_18 = True,
            spoiler = False,
            author_is_gold = False,
            author_mod = False,
            author_has_verified_email = True,
            permalink = "/r/wallstreetbets/comments/lfs22f/why_ill_never_stop_buying_gme_and_why_you/",
            author = "A_test_author",
            author_created = "2019-08-20T02:31:19Z",
            comment_karma = 2504),
            self.RedditModel(
            id = "qwerty",
            title = "This is a Test Title",
            content = "This is some Test Content",
            upvote_ratio = 0.77,
            score = 2625,
            num_comments = 580,
            created_on = "2021-02-09T02:08:58Z",
            stickied = False,
            over_18 = False,
            spoiler = False,
            author_is_gold = False,
            author_mod = False,
            author_has_verified_email = True,
            permalink = "/r/wallstreetbets/comments/lfs22f/why_ill_never_stop_buying_gme_and_why_you/",
            author = "A_test_author",
            author_created = "2019-08-20T02:31:19Z",
            comment_karma = 2504),
            self.RedditModel(
            id = "asdfxz",
            title = "This is a Test Title",
            content = "This is some Test Content",
            upvote_ratio = 0.77,
            score = 2625,
            num_comments = 580,
            created_on = "2021-02-09T02:08:58Z",
            stickied = False,
            over_18 = False,
            spoiler = False,
            author_is_gold = False,
            author_mod = False,
            author_has_verified_email = True,
            permalink = "/r/wallstreetbets/comments/lfs22f/why_ill_never_stop_buying_gme_and_why_you/",
            author = "A_test_author",
            author_created = "2019-08-20T02:31:19Z",
            comment_karma = 2504)
        ])

