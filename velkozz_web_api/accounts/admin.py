# Importing Dango Packages:
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

# Importing Custom User Data Model:
from .models import CustomUser

# Registering the Custom User Model to the admin dash:
admin.site.register(CustomUser, UserAdmin)