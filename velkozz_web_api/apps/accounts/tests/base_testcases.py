# Importing external testing packages:
import requests

# Importing Django Test packages: 
from django.test import TestCase
from accounts.models import CustomUser
from rest_framework.test import APIRequestFactory, force_authenticate
from django.contrib.auth.models import Group, Permission
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient

# Importing local methods for testing throtteling and request logging functions:
from utils.app_management import log_api_request
from django.urls import reverse
from django.conf import settings


class BaseAPITestCase(TestCase):
    """Object is meant to be extended by other test cases for the API.

    The object contains the boiler plate "setUp" code that performs the
    following config:

    - Creating the necessary permission groups.
    - Create several users, one for each permission group.
    - Assigning relevant permission groups to each user.
    - Creating the API test client that are used by child methods to perform
        api calls.

    TestCases that inherit this method can make use of all of these users, groups
    and permissions for testing purposes. This method contains the boilerplate authentication
    code for setting up a test environment.
    """
    def setUp(self):
        # Creating API permissions groups for testing based on the Accounts AppConfig:
        Group.objects.bulk_create([
            Group(name="api_free_tier"),
            Group(name="api_professional_tier"),
            Group(name="api_senior_tier"),
            Group(name="api_ingestion"),
            Group(name="api_developer")
        ])

        # Extracting the group objects for API users:
        self.api_free_tier = Group.objects.get(name="api_free_tier")
        self.api_professional_tier = Group.objects.get(name="api_professional_tier")
        self.api_senior_teir = Group.objects.get(name="api_senior_tier")
        self.api_ingestion = Group.objects.get(name="api_ingestion")
        self.api_developer = Group.objects.get(name="api_developer")

        # Creating users with differing permissions:
        CustomUser.objects.bulk_create([
            CustomUser(username="test_user_free", password="password123"),
            CustomUser(username="test_user_pro", password="password1233"),
            CustomUser(username="test_user_senior", password="password1234"),
            CustomUser(username="test_user_developer", password="password12345"),
            CustomUser(username="test_ingestion_account", password="ingestion_account")
        ])
        
        # Declaring all user objects as instance params:
        self.free_user = CustomUser.objects.get(username="test_user_free")
        self.prof_user = CustomUser.objects.get(username="test_user_pro")
        self.senior_user = CustomUser.objects.get(username="test_user_senior")
        self.ingestion_acc = CustomUser.objects.get(username="test_ingestion_account")
        self.developer = CustomUser.objects.get(username="test_user_developer")
    
        # Assigning permission groups to users:
        self.api_free_tier.user_set.add(self.free_user)
        self.api_professional_tier.user_set.add(self.prof_user)
        self.api_senior_teir.user_set.add(self.senior_user)
        self.api_ingestion.user_set.add(self.ingestion_acc)
        self.api_developer.user_set.add(self.developer)
        

        # Creating Authentication Tokens for each user:
        for user in CustomUser.objects.all():
            Token.objects.get_or_create(user=user)
       
        # Extracting the Throttle Rates from the Settings module:
        app_config = settings.REST_FRAMEWORK["GROUP_THROTTLE_RATES"]

        self.burst_rates = [
            app_config[throttle].split("/")[0] for throttle in app_config.keys()
            if "burst" in throttle]

        self.sustain_rates = [
            app_config[throttle].split("/")[0] for throttle in app_config.keys()
            if "sus" in throttle]

        # Declaring the Django Testing Client and associated urls:
        self.test_client = APIClient()
        