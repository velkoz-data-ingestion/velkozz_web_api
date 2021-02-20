# Importing external testing packages:
import requests

# Importing Django Test packages: 
from django.test import TestCase, Client
from accounts.models import CustomUser
from rest_framework.test import APIRequestFactory, force_authenticate
from django.contrib.auth.models import Group

# Importing local methods for testing throtteling and request logging functions:
from utils.app_management import log_api_request
from django.urls import reverse


class ThrottledAPIRequestTest(TestCase):
    """ 
    - Write startUp method that create users with several different categorie.
    """
    def startUp(self):
        """
        - Create two users: an api free tier and superuser and create authentication tokens for both users.
        - Use these requests to max out throttle requests and ensure that requests are denied. 
        """
        # Extracting the group objects for API users:
        api_free_tier = Group.objects.get(name="api_free_tier")
        api_professional_tier = Group.objects.get(name="api_professional_tier")

        # Creating users with differing permissions:
        test_user_free = CustomUser.objects.create_user(
            "test_user_free", "testuser@example.com", "password123")
        test_user_professional = CustomUser.objects.create_user(
            "test_user_pro", "protestuser@example.com", "password123")
        
        test_user_free.save()
        test_user_professional.save()

        # Assigning permission groups to users:
        api_free_tier.user_set.add(test_user_free)
        api_professional_tier.user_set.add(test_user_professional)

        # Extracting url routes to a test API endpoint:
        self.science_data_reddit_endpoint = reverse("social_media_api:reddit-rscienceposts")  

    def test_group_based_user_throtteling(self):
        pass
        
