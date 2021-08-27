# Importing Dango Packages:
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

# Importing Custom User Data Model:
from .models import CustomUser, APIApplication, APIRequestLog
from request.models import Request 

# Registering the Custom User Model to the admin dash:
admin.site.register(CustomUser, UserAdmin)

# Registering the API Services Models to the admin dash:
admin.site.register(APIApplication)
admin.site.register(APIRequestLog)