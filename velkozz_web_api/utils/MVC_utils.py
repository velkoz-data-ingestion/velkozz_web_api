

# TODO This is not viable due to different parameter names. Either find a way around this or give up and just write the code manually!
def filter_query_via_params(): 
    """The method is uses by the list and create (GET and POST) methods in 
    ViewSets to filter django model querysets via request parameters.

    The method extracts the necessaray parameters from the ingested request 
    object (assuming specific naming conventions) and filters the ingested
    queryset based on these specific parmas (again assuming specific naming
    conventions). This method is meant to contain the logic for the most common
    queryset filtering that takes place in the project, not to serve as an all
    encompassing purpose.

    Currently the method extracts and filters the following arguments:
    
    * Start-Date --> 
    * End-Date -->

    Args:
        request (HttpResponse): The response object made to the REST API that
            is passed through the ViewSet that needs to be filtered.

        queryset (QuerySet): The initial queryset of all django objects from
            the database.

    Returns:
        QuerySet: The filtered queryset of the data model.
    """
    pass