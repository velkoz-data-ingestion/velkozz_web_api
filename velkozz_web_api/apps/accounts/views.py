# Importing Django Packages:
from django.shortcuts import render, redirect
from rest_framework import viewsets
from django.db import models
from django.contrib import auth
from django.contrib.auth.models import Permission
from django.apps import apps
from django.http import HttpResponse, HttpResponseRedirect

# DRF Packages:
from rest_framework.permissions import IsAuthenticated
from .permissions import HasAPIAccess
from .throttles import APIBurstUserPermissionGroupsThrottle, APISustainedUserPermissionGroupsThrottle  

# Importing app specific utility:
from utils.app_management import get_user_api_app_permissions

# Importing Database Model:
from accounts.models import APIApplication
from social_media_api.apps import SocialMediaAPIConfig
from finance_api.apps import FinanceApiConfig


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

# Main Frontend views:
def site_main_index(request):
    context = {}
    return render(request, "accounts/site_index.html", context)

def account_index(request):
    context = {}

    # Extracting the list of only API apps the user has access to:
    #user_permission = request.user.get_user_permissions()
    #user_api_app_permissions = get_user_api_app_permissions(user_permission)
    
    # Querying the API Application Database Model based on the models the user has access to:
    available_api_apps = APIApplication.objects.all()

    # Populating the Context:
    context["api_permissions"] = available_api_apps

    return render(request, "accounts/account_index.html", context)

def account_dashboard(request):
    """The view for the user account dashboard.
    """
    # Creating an empty context to be populated:
    context = {}
    
    return render(request, 'accounts/user_account_dashboard.html', context=context)

# API Documentation views:
def api_docs(request, api_name):
    """View that uses a doc id string parameter to determine
    which documentation html file to render. 

    Arguments:
        request ():

        api_name (str): The string that is recieved from the url that
            is parsed and used to determine which html template to 
            render.

    """
    # Declaring main dict of all api app names: api doc template path:
    api_doc_dict = {
        SocialMediaAPIConfig.name : "accounts/docs/social_media_api_docs.html",
        FinanceApiConfig.name : "accounts/docs/finance_data_api_docs.html"
    }

    return render(request, api_doc_dict[api_name])

# User Management views:
def account_login(request):
    """View that hosts the custom login page for users
    """
    return render(request, "accounts/login.html")

def account_create(request):
    """View that renders the custom user creation page.
    """
    return render(request, "accounts/create_account_form.html")

def account_auth(request):
    """Custom login method that overwrites django defaul login route
    """
    # Extracting the username and password from the POST form:
    username = request.POST.get("username", "")
    pswrd = request.POST.get("password", "")

    # Authentication of the user, to check if it's active or None
    user = auth.authenticate(username=username, password=pswrd)

    # if the user is validated loggin in the user:
    if user is not None:
        if user.is_active:
            auth.login(request, user)

            return redirect("main_index")

    else:
        return redirect("login_page")


