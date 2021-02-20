# Importing django settings module to extract conf params:
from django.conf import settings

# Importing DRF throtteling methods:
from rest_framework.throttling import UserRateThrottle

# Importing internal django models:
from accounts.models import APIRequestLog

# Importing utility packages:
from utils.app_management import log_api_request, get_api_throttle_scope 


class APIBurstUserPermissionGroupsThrottle(UserRateThrottle):
    """
    - API Throttle makes assumptions about group naming conventions. (Assumes group names relevant to
        api permissions always contain the preface "api").

    """
    def __init__(self): 

        # Declaring external list of permission groups:
        rst_framework_dict = getattr(settings, "REST_FRAMEWORK", None)
        self.THROTTLE_RATES = rst_framework_dict["GROUP_THROTTLE_RATES"]

        # Extracting list of potential scopes to be parsed in 'get_cache_key:
        self.scope = list(self.THROTTLE_RATES.keys())[0]
        self.throttle_rate_names = list(self.THROTTLE_RATES.keys())

        # Initalizing UserRateThrottle:
        super().__init__()

    def get_cache_key(self, request, view):
        
        ident = self.get_ident(request)

        # Extracting a list of all group names::
        user_groups = [group.name for group in request.user.groups.all()]
        try:

            # Re-declaring the scope of the throttle based on user Group:
            self.scope = get_api_throttle_scope(user_groups, self.throttle_rate_names, "burst")
            
            # Assigning a throttle rate for the new scope variable:
            self.rate = self.THROTTLE_RATES[self.scope]
            ident = request.user.username

        except Exception as e:
            print(e)

        return self.cache_format % {
            'scope': self.scope,
            'ident': ident
        }        

    def allow_request(self, request, view):
        # Implementing the internal throttle validation method:
        base_validation = super(APIBurstUserPermissionGroupsThrottle, self).allow_request(request, view)

        # If the base validation is validated log request:
        if base_validation == True:
            log_api_request(request, APIRequestLog)

        return base_validation
    
class APISustainedUserPermissionGroupsThrottle(UserRateThrottle):
    """
    - API Throttle makes assumptions about group naming conventions. (Assumes group names relevant to
        api permissions always contain the preface "api").

    """
    def __init__(self): 

        # Declaring external list of permission groups:
        rst_framework_dict = getattr(settings, "REST_FRAMEWORK", None)
        self.THROTTLE_RATES = rst_framework_dict["GROUP_THROTTLE_RATES"]

        # Extracting list of potential scopes to be parsed in 'get_cache_key:
        self.scope = list(self.THROTTLE_RATES.keys())[0]
        self.throttle_rate_names = list(self.THROTTLE_RATES.keys())
        
        # Initalizing UserRateThrottle:
        super().__init__()

    def get_cache_key(self, request, view):
        
        ident = self.get_ident(request)

        # Extracting a list of all group names::
        user_groups = [group.name for group in request.user.groups.all()]
        try:

            # Re-declaring the scope of the throttle based on user Group:
            self.scope = get_api_throttle_scope(user_groups, self.throttle_rate_names, "sus")
            
            # Assigning a throttle rate for the new scope variable:
            self.rate = self.THROTTLE_RATES[self.scope]
            ident = request.user.username

        except Exception as e:
            print(e)

        return self.cache_format % {
            'scope': self.scope,
            'ident': ident
        }        

    def allow_request(self, request, view):
        # Implementing the internal throttle validation method:
        base_validation = super(APISustainedUserPermissionGroupsThrottle, self).allow_request(request, view)

        # If the base validation is validated log request:
        if base_validation == True:
            log_api_request(request, APIRequestLog)

        return base_validation