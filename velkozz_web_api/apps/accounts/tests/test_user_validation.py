# Importing Django Test packages: 
from django.test import TestCase, Client
from rest_framework.test import APIRequestFactory, force_authenticate

# Importing local methods for testing sucessful user auth and permissions:

# Importing local methods for testing throtteling and request logging functions:
from utils.app_management import log_api_request


class ThrottledAPIRequestTest(TestCase):
    """
    - Write startUp method that create users with several different categorie.
    """
    def startUp(self):
        pass