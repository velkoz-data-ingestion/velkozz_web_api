
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
    """
    - Extract all features of the api request from the http request object.
    - Write the API request to the database. 
    """
    pass 