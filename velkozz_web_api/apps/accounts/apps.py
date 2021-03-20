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
        """
        # Importing the Django Auth models:
        from django.contrib.auth.models import Group
        #from accounts.models import CustomUser

        # TODO: Determine if this should be done hardcoded or after init in database:
        # API user permissions:
        Group.objects.update_or_create(name="api_free_tier")
        Group.objects.update_or_create(name="api_senior_tier")
        Group.objects.update_or_create(name="api_professional_tier")

        # API Developer permission groups:
        Group.objects.update_or_create(name="api_ingestion")
        Group.objects.update_or_create(name="api_developer")
        """
