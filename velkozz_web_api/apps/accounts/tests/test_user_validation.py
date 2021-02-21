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
from .base_testcases import BaseAPITestCase
from utils.app_management import log_api_request
from django.urls import reverse
from django.conf import settings




class ThrottledAPIRequestTest(BaseAPITestCase):
    """TestCase that tests the functionality of the custom
    user group based throttles. 
    """
    def setUp(self):
        
        # Initalizing parent setUp method:
        super().setUp()

        self.api_url = "/social_media_api/reddit/rscience/"

    def test_group_based_user_throtteling(self): 
        """Performs GET requests to an API endpoint to test dynamic scope throttles based
        on specific user groups. 

        Uses the social media reddit endpoint for testing.
        """
        # Assigning science post moddel permissions to free tier user:
        permissions = Permission.objects.all().filter(name__contains="science posts")
        for permission in permissions:
            self.free_user.user_permissions.add(permission)

        # Authenticating the APICilent for the free tier user:
        user_token = Token.objects.get(user=self.free_user)
        self.test_client.credentials(HTTP_AUTHORIZATION=f'Token {user_token.key}')
        
        inital_response = self.test_client.get(self.api_url)

        # Asserting that the request was validated:
        self.assertEqual(200, inital_response.status_code)

        # Iterating attempting to get burst free tier user to throttle: 
        for _ in range(int(self.burst_rates[0])):
            response = self.test_client.get(self.api_url)

        # Asserting that the response has been sucessfully throttled:
        self.assertEqual(429, response.status_code)
    
    def test_throttle_logging(self):
        """Performs standard ingestion to an API endpoint and then tests
        the ability of the User Group Throttle to log all validated request
        to the database.
        """
        pass

        
        
                