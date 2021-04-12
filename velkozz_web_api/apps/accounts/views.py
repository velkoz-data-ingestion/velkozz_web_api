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
from request.models import Request

# Importing 3rd party packages:
import pandas as pd
from datetime import date, timedelta

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

def staff_dash(request):
    """Route for displaying the staff dashboard of the site.
    """
    # Empty context to populate:
    context = {}

    # Ensuring that the user is a staff member if not redirect home:
    if request.user.is_staff is False:
        return redirect("user_account_dashboard")
    
    else:

        # Determining a one month window for queying request data:
        prev_month = date.today() - timedelta(days=30)

        # Querying all of the requests made to the database in the last month:
        max_queryset = Request.objects.filter(time__gt=prev_month)

        # QuerySet to Dataframe Conversions:
        requests_timeseries = max_queryset.values_list("time", "response", "method", "path", "user")
        timeframe_df = pd.DataFrame.from_records(requests_timeseries, columns=["time", "response", "method", "path", "user"])
        timeframe_df["_count"] = 1
        timeframe_df.set_index(timeframe_df['time'], inplace=True)

        # Resampling/Transforming data:
        daily_resample_get = timeframe_df.loc[timeframe_df['method'] == 'GET', "_count"].squeeze().resample('H').sum()
        daily_resample_posts = timeframe_df.loc[timeframe_df['method'] != 'GET', "_count"].squeeze().resample('H').sum()

        # Seralzing dataframe columns to pass to template:
        context['get_datetime'] = daily_resample_get.index.tolist()
        #context['post_datetime'] = daily_resample_posts.index.tolist()
        
        # Popularing Context:
        context['get_requests_count'] = daily_resample_get.values.tolist()
        context['post_requests_count'] = daily_resample_posts.values.tolist()

        return render(request, "accounts/staff_dashboard.html", context)