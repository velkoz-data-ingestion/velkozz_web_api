from rest_framework.throttling import UserRateThrottle

# TODO: Build Out Skeleton for Throtteling Frameworks based on file outline.

# User Tier Subscription Throttle Classes:
class BaseAPITierThrottle(UserRateThrottle):
    """
    - Ingest the request and check if the associated user is part of the assigned group. If they are, return true.
    - Once the user is validated, call a function that writes the request to the database for each user.
    """
    pass


class APIFreeTierMinThrottle():
class APIFreeTierDayThrottle():

class APISeniorTierMinThrottle(UserRateThrottle):
class APISeniorTierDayThrottle(UserRateThrottle):

class APIProfessionalTierMinThrottle(UserRateThrottle):
class APIProfessionalTierMinThrottle(UserRateThrottle):

class APIDataIngestionThrottle(UserRateThrottle):

class APIDeveloperThrottle(UserRateThrottle):

        
