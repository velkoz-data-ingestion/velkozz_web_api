# Importing Django Packages:
from django.shortcuts import render
from rest_framework import viewsets
from django.db import models
from django.contrib.auth.models import Permission
from django.apps import apps

# DRF Packages:
from rest_framework.permissions import IsAuthenticated
from .permissions import HasAPIAccess
from .throttles import APIBurstUserPermissionGroupsThrottle, APISustainedUserPermissionGroupsThrottle  

# Importing app specific utility:
from utils.app_management import get_user_api_app_permissions

# Importing Database Model:
from accounts.models import APIApplication


class AbstractModelViewSet(viewsets.ModelViewSet):
    """A ModelViewSet object that serves as an abstract
    ModelViewSet for all ViewSets used in the REST APIs in
    the project.

    This object is not intended to serve as an actual initalized
    ModelViewSet, just as a parent for other methods.
    """
    # Adding Custom Permissions for the ModelViewSet:
    permission_classes = [IsAuthenticated, HasAPIAccess]
    
    # Adding Custom Throttling for the ModelViewSet:
    throttle_classes = [APIBurstUserPermissionGroupsThrottle, APISustainedUserPermissionGroupsThrottle]


def site_main_index(request):
    context = {}
    return render(request, "accounts/site_index.html", context)


def account_index(request):
    context = {}

    # Extracting the list of only API apps the user has access to:
    user_permission = request.user.get_user_permissions()
    user_api_app_permissions = get_user_api_app_permissions(user_permission)
    
    # Querying the API Application Database Model based on the models the user has access to:
    available_api_apps = APIApplication.objects.filter(module_name__in=user_api_app_permissions)

    # Populating the Context:
    context["api_permissions"] = available_api_apps

    return render(request, "accounts/account_index.html", context)

# API Documentation views:
def social_media_docs(request):
    return render(request, "accounts/docs/social_media_api_docs.html")
    
def finance_docs(request):
    return render(request, "accounts/docs/finance_data_api_docs.html")
