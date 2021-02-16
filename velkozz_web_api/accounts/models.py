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