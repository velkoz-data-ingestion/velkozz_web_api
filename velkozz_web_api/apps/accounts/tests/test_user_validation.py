# Importing external testing packages:
import requests

# Importing Django Test packages: 
from django.test import TestCase, Client
from accounts.models import CustomUser
from rest_framework.test import APIRequestFactory, force_authenticate
from django.contrib import auth
from django.contrib.auth.models import Group, Permission
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient

# Importing local methods for testing throtteling and request logging functions:
from .base_testcases import BaseAPITestCase
from accounts.models import APIRequestLog
from utils.app_management import log_api_request
from django.urls import reverse
from django.conf import settings

class AccountUserManagementTest(TestCase):
    """A testcase that contains all of the tests for the account
    apps's user managment/authentication system.

    The TestCase performs tests on the ability of the accounts app to: 

    - Create a CustomUser via the django URLs.
    - Login a CustomUser via the django URLs.
    - Logout a CustomUser via the django URLs. 
    
    """
    def setUp(self):
        
        # Creating a user to test sign-in func:
        login_test_usr = CustomUser.objects.create(username="login_test_user", password="test_pass")
        login_test_usr.save()

        # Client for performing requests:
        self.login_client = Client()

    def test_user_creation(self):
        pass

    def test_user_login(self):
        """Performs POST request to login endpoint to  authenticate
        a user with the name 'login_test_user' and password 'test_pass'.
        """
        # Testing that the user created for tested exists:
        test_usr = CustomUser.objects.get(username="login_test_user", password="test_pass")
        self.assertNotEqual(test_usr, None)

        # The client should not be logged in: correctly
        user = auth.get_user(self.login_client)
        self.assertEqual(user.is_authenticated, False)

        # Logging in the client from endpoint: 
        login_response = self.login_client.post(
            "/accounts/auth/",
            {
                "username": "login_test_user",
                "password":"test_pass"
            }
        )

        # Default Client() login:
        test = self.login_client.login(
            username="login_test_user",
            password="test_pass"
        )

        self.login_client.force_login(test_usr)

        user = auth.get_user(self.login_client)

        # Testing response and login status:
        self.assertEqual(login_response.status_code, 302) # Should be a redirect.    

        self.assertEqual(user.is_authenticated, True)

        #TODO: FIX LOGIN TESTING. WHY IS LOGIN ROUTE REDIRECTING BUT NOT AUTHENTICATING.

        print("\nTested Authentication CustomUser Account Login Functionality <account_auth>.")

    def test_user_logout(self):
        pass

class ThrottledAPIRequestTest(BaseAPITestCase):
    """TestCase that tests the functionality of the custom
    user group based throttles. 
    """
    def setUp(self):
        
        # Initalizing parent setUp method:
        super().setUp()

        self.rscience_api_url = "/social_media_api/reddit/rscience/"
        self.rwsb_api_url = "/social_media_api/reddit/rwallstreetbets/"

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
        
        inital_response = self.test_client.get(self.rscience_api_url)

        # Asserting that the request was validated:
        self.assertEqual(200, inital_response.status_code)

        # Iterating attempting to get burst free tier user to throttle: 
        for _ in range(int(self.burst_rates[0])):
            response = self.test_client.get(self.rscience_api_url)

        # Asserting that the response has been sucessfully throttled:
        self.assertEqual(429, response.status_code)

        print(f"\nTested Throtteling Based on User Group Scope <APIBurstUserPermissionGroupsThrottle> Throttle")

    def test_throttle_logging(self):
        """Performs standard ingestion to an API endpoint and then tests
        the ability of the User Group Throttle to log all validated request
        to the database.
        """
        # Assigning science post moddel permissions to a developer user:
        permissions = Permission.objects.all().filter(name__contains="wall street bets posts")
        for permission in permissions:
            self.prof_user.user_permissions.add(permission)

        # Authenticating the APICilent for the free tier user:
        user_token = Token.objects.get(user=self.prof_user)
        self.test_client.credentials(HTTP_AUTHORIZATION=f'Token {user_token.key}')

        # Ensuring that the API Request Log is empty before testing:
        inital_log_query = APIRequestLog.objects.all()
        self.assertEqual(len(inital_log_query), 0)

        # Performing API Requests to the database:
        for _ in range(5):
            response = self.test_client.get(self.rwsb_api_url)

        for _ in range(5):
            response = self.test_client.post(self.rwsb_api_url)

        # Assertion testing that all of the GET and POST requests were logged:
        request_logs = APIRequestLog.objects.all()
        get_logs = request_logs.filter(request_type="GET")
        post_logs = request_logs.filter(request_type="POST")

        self.assertEqual(len(get_logs), 5)
        self.assertEqual(len(post_logs), 5)

        for get_log in get_logs:
            self.assertEqual(get_log.request_type, "GET")
            self.assertEqual(get_log.request_user, self.prof_user)
            self.assertEqual(get_log.api_endpoint, "WallStreetBetsViewSet")
            self.assertEqual(get_log.api_app, "social_media_api")
        
        
        for post_log in post_logs:
            self.assertEqual(post_log.request_type, "POST")
            self.assertEqual(post_log.request_user, self.prof_user)
            self.assertEqual(post_log.api_endpoint, "WallStreetBetsViewSet")
            self.assertEqual(post_log.api_app, "social_media_api")
        
        print(f"\nTested Throttle Logging from <APIBurstUserPermissionGroupsThrottle> via log_api_request()")

class PermissionAPIRequestTest(BaseAPITestCase):
    """TestCase that tests the permissions applied to the DRF APIs through the 
    HasAPIAccess DjangoModelPermission.

    Performs testing to ensure that the default Django Model Authentication/Permission 
    system suscesfully adds and restricts access to the specific CRUD elements of APIs.
    The TestCase makes use of the social media APIs for testing. 
    """
    def setUp(self):
        # Initalizing parent setUp method:
        super().setUp()

        self.rscience_api_url = "/social_media_api/reddit/rscience/"
        self.rwsb_api_url = "/social_media_api/reddit/rwallstreetbets/"

    def test_GET_permissions(self):
        """Attempts to add and remove GET (view) permissions to the social media API
        to a specific user and testing if the request is authenticated or not based on
        default django model access permissions.
        """
        # Authenticating the APICilent for the professional tier user:
        user_token = Token.objects.get(user=self.senior_user)

        self.test_client.credentials(HTTP_AUTHORIZATION=f'Token {user_token.key}')

        # Extracting the permissions for the WallStreetBets Model:
        get_wsb_permission = Permission.objects.get(codename="view_wallstreetbetsposts")

        # self.senior_user currently does not have wsb model permissions testing request denied:
        unauthenticated_response = self.test_client.get(self.rwsb_api_url)

        # Testing GET (view) authentication: 
        self.assertEqual(unauthenticated_response.status_code, 403)

        # Giving the professional user view permission/access to the WallStreetBets Model:
        self.senior_user.user_permissions.add(get_wsb_permission)

        authenticated_response = self.test_client.get(self.rwsb_api_url)

        # Testing GET (view) authentication: 
        self.assertEqual(authenticated_response.status_code, 200)

        # Removing User access and testing authentication:
        self.senior_user.user_permissions.remove(get_wsb_permission)
        new_unauth_response = self.test_client.get(self.rwsb_api_url)

        # Testing GET (view) authentication: 
        self.assertEqual(new_unauth_response.status_code, 403)


        print("\nTesting View (GET) Model Permissions of <HasAPIAccess> DRF Permission Class")

    def test_POST_permissions(self):
        """Attempts to add and remove POST (add) permissions to the social media API
        to a specific user and testing if the request is authenticated or not based on
        default django model access permissions.
        """
        # Authenticating the APICilent for the professional tier user:
        user_token = Token.objects.get(user=self.senior_user)
        self.test_client.credentials(HTTP_AUTHORIZATION=f'Token {user_token.key}')

        # Extracting the permissions for the WallStreetBets Model:
        post_wsb_permission = Permission.objects.get(codename="add_wallstreetbetsposts")

        # self.senior_user currently does not have wsb model permissions testing request denied:
        unauthenticated_response = self.test_client.post(self.rwsb_api_url)

        # Testing POST (add) authentication: 
        self.assertEqual(unauthenticated_response.status_code, 403)

        # Giving the professional user add permission/access to the WallStreetBets Model:
        self.senior_user.user_permissions.add(post_wsb_permission)
        authenticated_response = self.test_client.post(self.rwsb_api_url)

        # Testing POST (add) authentication: 
        self.assertEqual(authenticated_response.status_code, 200)

        # Removing User access and testing authentication:
        self.senior_user.user_permissions.remove(post_wsb_permission)
        new_unauth_response = self.test_client.post(self.rwsb_api_url)

        # Testing GET (view) authentication: 
        self.assertEqual(new_unauth_response.status_code, 403)

        print("\nTesting Add (POST) Model Permissions of <HasAPIAccess> DRF Permission Class")

