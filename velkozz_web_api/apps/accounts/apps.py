# Importing Django Packages:
from django.apps import AppConfig

# Importing data models for startup configuration:
#from django.contrib.auth.models import Group

class UserAccountConfig(AppConfig):
    name = 'accounts'
    verbose_name = "User Accounts Application"
