
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

        # Unpacking request for relevant fields:
        api_log_database_model.objects.create(
            request_user = request.user,
            request_type = request.method, 
            api_application = request.current_app)
            
        api_log_database_model.save()

    else:
        return AttributeError(f"API Ingestion method someone was passed a non-authenticated request!!! from {request.user.get_username()}")