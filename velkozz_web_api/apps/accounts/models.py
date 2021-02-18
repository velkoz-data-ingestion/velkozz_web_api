# Importing Django Packages:
from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    pass

class APIApplication(models.Model):
    """The Database Model representing information for each API service
    app.

    The model is only populated on the backend by each API applications
    AppConfig object via the AppConfig.ready() method which writes a 
    static set of data to the database upon server startup.

    Attributes:
        module_name (models.CharField): The non-verbose name of the module. This
            is the string that is used to configure the url route to the main endpoint
            of the API app.  

        app_name (models.CharField): The verbose name of the module. This is
            written from the APIConfig.verbose_name field.
        
        app_description (models.TextField): The long-form description of the 
            api application that is written from the APIConfig.description field.

    """
    module_name = models.CharField(max_length=200, primary_key=True)
    app_name = models.CharField(max_length=200, unique=True)
    app_description = models.TextField()

    def __str__(self):
        return self.app_name

    class Meta:
        verbose_name_plural = "API Applications"

class APIRequestLog(models.Model):
    """The Database Model representing a timeseries of requests made to each 
    data api.

    This database module is populated via a ingestion function called in viewset
    Throttler. Queries are made against this data model to build a timeseries
    graph showing the amount of requests to an API a specific user makes. 

    Attributes:
        request_user (models.ForeginKey): The foregin key that connects to an instance of the
            application's user model. (CustomUser).
        
        request_type (models.CharField): The type of request that was made to the API
            (eg: GET, POST).
        
        request_time (models.DateTimeField): The date and time when the request was made.

        api_application (models.CharField): The name of the API application that the request 
            was made to.

    """
    request_user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    request_type = models.CharField(max_length=10)
    request_time = models.DateTimeField(auto_now_add=True)
    api_application = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.request_user}_{self.request_time}_{api_application}"