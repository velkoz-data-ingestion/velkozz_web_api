# Importing Django Packages:
from django.apps import AppConfig

# Importing data models for startup configuration:
#from django.contrib.auth.models import Group

class UserAccountConfig(AppConfig):
    name = 'accounts'
    verbose_name = "User Accounts Application"

    def ready(self):
        """
        Upon app startup the method creates several groups in the django 
        authentication system. 

        These groups are the backbone of the DRF permission system that is
        used for API service access and throtteling. The permissions are 
        created with their key Many-to-Many field empty as it should be
        manually populated to include permissions for each API group.

        """
        pass