from rest_framework.throttling import UserRateThrottle

# User Tier Subscription Throttle Classes:
class BaseAPIUserThrottle(UserRateThrottle):
    """
    - Ingest the request and check if the associated user is part of
        the assigned group. If they are, return true.
    - Once the user is validated, call a function that writes the request to the database for each user.
    """
