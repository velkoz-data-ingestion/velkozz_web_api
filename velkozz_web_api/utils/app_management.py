# Importing Django packages:
from django.urls import resolve
from django.apps import apps
from django.conf import settings

# Method that extracts a list of all API apps for the project:
def get_user_api_app_permissions(permission_lst):
    """A method that parses a permission set to extract a subset
    of API apps.

    The method iterates over a set of permission strings, usually extracted
    from a .get_permissions() method and removes every permission string that
    does not contain the substring "api". The use case for this function would
    be to get the list of API apps that a user or group has access to.

    The method contains very little type checking and assumes a specific data format
    that conforms to the outputs from django methods such as `user.get_user_permissions()`

    Example:
        user_permission = user.get_user_permissions() <-- {'sessions.add_session', 'finance_api.add_djiaindexcomposition'}
        api_permission = get_user_api_app_permissions(user_permission)

        api_permission <-- {'finance_api'}

    Arguments:
        permission_lst (set): A set of strings that typically contains permission string
            names. 
    
    Returns:
        set: The set containing only api app name.   

    """
    # Using list comprehension to extract only app name from api model permissions:
    api_app_permission_lst = [
        permission_str.split(".", 1)[0] for permission_str in permission_lst 
        if "api" in permission_str if "accounts" not in permission_str]
    
    # Converting list to set to extract only unique elements of the api permissions lst:
    api_app_permissions = set(api_app_permission_lst)

    return api_app_permissions

# Method that ingests a request and writes the request to a database table:
def log_api_request(request, api_log_database_model):
    """A method that writes an api request to a database using a specific django
    data model.

    The method is meant to serve as a de-facto logging function for all incoming
    HTTP Requests to an API that is validated by a DRF Throtteling object. The method
    extracts features from the request parameter and creates an instance of the 
    api_log_database_model django model. This model instance is then saved to the database.

    The method is designed for a very specific use case and as such it makes very strict 
    assumptions about the structure of the data model `api_log_database_model`
    (it assumes the data model being passed in is APIRequestLog).
    
    Attributes:
        request (HttpRequest): A django object representing an Http Request. For the method
            it is a request made to an API endpoint that has passed through the throtteling
            class.
        
        api_log_database_model (django.db.models.Modle): The model that will be used to store
            all API requests that are not throttled. Assumed to be APIRequestLog model.
            
    """
    # Enuring that the request user is authenticated for redundant authentication:
    if request.user.is_authenticated:
        
        # Extracting the full path to the specific request function:  
        url_resolver = resolve(request.path)._func_path 
        
        # Parsing the view function path to extract App name and ModelView:
        # Makes HEAVY assumptions about the structure of funtion path:
        func_path_lst = url_resolver.split(".")
        app_name = func_path_lst[1]
        api_name = func_path_lst[-1]

        # Unpacking request for relevant fields:
        api_log = api_log_database_model.objects.create(
            request_user = request.user,
            request_type = request.method, 
            api_app = app_name,
            api_endpoint= api_name
        )

        api_log.save()

    else:
        raise AttributeError(f"API Ingestion method someone was passed a non-authenticated request!!! from {request.user.get_username()}")
        
def get_api_throttle_scope(user_groups_lst, api_throttle_rates, throttle_type):
    """Method searches two lists in O(n) time for an api throttle scope based on
    the user's Permission Group. This inefficient search is possible due to how
    short the lists are.

    The method is used by custom throttle object to select the throttle scope for API Views.
    The method is designed to be used by both a burst and sustained throttle class and as such
    the "burst" or "sustained" throttle scope is selected via the type param.

    Arguments: 
        user_groups_lst (list): A list containing all of the Groups the user is apart of. It assumes
            that their is only one commone element (one relßevant permission group) between this list
            and api_throttle_rates.

        api_throttle_rates (list): A list containing all of the possible throttle rate scopes extracted
            from the settings GROUP_THROTTLE_RATES.keys() param in the Throttle class. Only one element
            from this list will be returned as the appropriate scope.

        throttle_type (str): The type of throttle scope that will be returned if the relevant throttle scopes are 
            found. It is designed so that the method should select either a "sus" or "burst" scope based
            on sub-string selection. 

    Returns:
        string: The name of the selected throttle scope.
    """
    # Iterating through all users searching for str of format: "{user_group}_min":
    for user_group in user_groups_lst:
        for api_throttle_rate in api_throttle_rates:

            if user_group and throttle_type in api_throttle_rate:
                return api_throttle_rate
                
            else:
                pass


    