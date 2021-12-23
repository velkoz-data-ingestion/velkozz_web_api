# Importing Django Packages:
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from rest_framework import viewsets
from django.db import models
from django.contrib import auth
from django.contrib.auth.models import Permission
from django.conf import settings
from django.apps import apps
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.urls import resolve 

# DRF Packages:
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from .permissions import HasAPIAccess
from .throttles import APIBurstUserPermissionGroupsThrottle, APISustainedUserPermissionGroupsThrottle  

# Importing app specific utility:
from utils.app_management import get_user_api_app_permissions

# Importing Database Model:
from accounts.models import APIApplication
from social_media_api.apps import SocialMediaAPIConfig
from finance_api.apps import FinanceApiConfig
from news_api.apps import NewsApiConfig
from request.models import Request

# Importing Seralizers for Request Logs: 
from accounts.account_serializers import RequestSerializer, SettingsSerializer

# Importing 3rd party packages:
import pandas as pd
from datetime import date, timedelta
import time
from operator import and_, or_
from functools import reduce

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

@login_required
def account_dashboard(request):
    """The view for the user account dashboard.
    """
    # Creating an empty context to be populated:
    context = {}

    # Ensuring that the user is a staff member if not redirect home:
    if request.user.is_authenticated is False:
        return redirect("main_index")
    

    # Querying the user permission groups:
    for group in request.user.groups.all():
        # Isolating the user tier groups:
        if "tier" in group.name:
            context["api_group"] = group

    # Querying the API key for the given user:
    try:
        context["user_api_token"] = Token.objects.get(user=request.user)
    except Exception:
        context["user_api_token"] = None 

    # Get a list of View Permissions for specific user:
    context["model_permissions"] = request.user.get_all_permissions()

    # Determining a one month window for queying request data:
    prev_week = date.today() - timedelta(days=7)

    # Querying all of the requests made to the database in the last week:
    request_queryset = Request.objects.filter(time__gt=prev_week).filter(user=request.user)
    
    # Filtering QuerySet to only contain requests to the API:
    request_queryset = request_queryset.filter(reduce(or_, [
        models.Q(path__icontains=app.module_name) for app in APIApplication.objects.all()]))

    # Converting the request queryset to a dataframe for formatting:
    user_request_values = request_queryset.values_list("time", "path")
    user_req_df = pd.DataFrame.from_records(user_request_values, index="time", columns=["time","path"])
    # Adding counter variable for resampling:
    user_req_df["_counter"] = 1

    #TODO: Fix this Resampling. Producing List of lists instead of just list.

    # TODO: Create a query for Reddit Pipeline ETL that is used to plot the graphs of Reddit Data Ingestion.


    # logic to not resample if index is broken (eg: There is no data so index is an empty list):
    if len(user_req_df) < 2:
           return render(request, 'accounts/user_account_dashboard.html', context=context)
    
    else:
        #print(user_req_df["_counter"].squeeze())
        hour_resample = user_req_df["_counter"].squeeze().resample("H").sum()
        daily_resample = user_req_df["_counter"].squeeze().resample("D").sum()

        # Populating context for the user requests:
        context["user_req_hourly"] = {
            "Data" : hour_resample.values.tolist(),
            "Index" : hour_resample.index.tolist()
        }

        context["user_req_daily"] = {
            "Data" : daily_resample.values.tolist(),
            "Index" : daily_resample.index.tolist()
        }

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
        FinanceApiConfig.name : "accounts/docs/finance_data_api_docs.html",
        NewsApiConfig.name: "accounts/docs/news_data_api_docs.html"
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

@login_required
def staff_dash(request):
    """Route for displaying the staff dashboard of the site.
    """
    # Empty context to populate:
    context = {}

    def get_account_name(path):
        """Method contains logic to extract the app name from a url path.
        
        Method uses the django.urls.resolve method with basic string splitting.
        """
        try:
            appname = resolve(path).func.__module__.split(".")[1]
        except:
            appname = None

        return appname

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
        
        # Adding columns:
        timeframe_df["_count"] = 1
        timeframe_df['app'] = timeframe_df["path"].apply(lambda x: get_account_name(x)) 
        timeframe_df.set_index(timeframe_df['time'], inplace=True)

        # Resampling/Transforming data:
        daily_resample_get = timeframe_df.loc[timeframe_df['method'] == 'GET', "_count"].squeeze().resample('H').sum()
        daily_resample_posts = timeframe_df.loc[timeframe_df['method'] != 'GET', "_count"].squeeze().resample('H').sum()

        # Extracting Series for all response codes:
        daily_200_response = timeframe_df.loc[timeframe_df["response"] < 300, "_count"]

        daily_300_response = timeframe_df.loc[
            (timeframe_df["response"] >= 300) & (timeframe_df["response"] < 400), "_count"]

        daily_400_response = timeframe_df.loc[
            (timeframe_df["response"] >= 400) & (timeframe_df["response"] < 500), "_count"]
       
        daily_500_response = timeframe_df.loc[timeframe_df["response"] >= 500, "_count"]

        # Building a dict of unique get/post timeseries based on unique apps:
        app_timeseries_dict = {}

        # Getting relevant list of installed apps:
        third_party_apps = [app.split(".")[0] for app in settings.INSTALLED_APPS
            if not app.startswith("django.") and
            app not in ['rest_framework', 'rest_framework.authtoken', 'rest_auth', 'request']
            ]

        for app in third_party_apps:
            
            # Nested dict structure for GET and POST request storage:
            application_dict = {}

            # Populating application dict w/ GET and POST request timeseries:
            try:
                app_timeseries_get = timeframe_df.loc[
                    (timeframe_df["app"] == app) & (timeframe_df["method"] == "GET"), "_count"].resample("H").sum()
                application_dict["GET"] = {
                    "Data" : app_timeseries_get.values.tolist(),
                    "Index": app_timeseries_get.index.tolist()
                    }
                
            except:
                application_dict["GET"] = [0] * len(daily_resample_get.index)
            
            try:    
                app_timeseries_post = timeframe_df.loc[
                    (timeframe_df["app"] == app) & (timeframe_df["method"] == "POST"), "_count"].resample("H").sum()
                application_dict["POST"] = {
                    "Data": app_timeseries_post.values.tolist(),
                    "Index": app_timeseries_post.index.tolist()
                    }
            except:
                application_dict["POST"] = [0] * len(daily_resample_get.index)

            # Fully Building nested dict:
            app_timeseries_dict[app] = application_dict
            print(len(application_dict["GET"]["Data"]), len(application_dict["GET"]['Index']))


        # Seralzing dataframe columns to pass to template:
        context['get_datetime'] = daily_resample_get.index.tolist()

        # Error-Catching daily response codes when resampling:
        response_code_dict = {}
        try:
            response_code_dict[200] = daily_200_response.squeeze().resample("H").sum().values.tolist()
        except Exception:
            response_code_dict[200] = [0] * len(daily_resample_get.index)

        try:
            response_code_dict[300] = daily_300_response.squeeze().resample("H").sum().values.tolist()
        except Exception:
            response_code_dict[300] = [0] * len(daily_resample_get.index)

        try:
            response_code_dict[400] = daily_400_response.squeeze().resample("H").sum().values.tolist()
        except Exception:
            response_code_dict[400] = [0] * len(daily_resample_get.index)

        try:
            response_code_dict[500] = daily_500_response.squeeze().resample("H").sum().values.tolist()
        except Exception:
            response_code_dict[500] = [0] * len(daily_resample_get.index)
        
        # Populating Context:
        context['app_timeseries'] = app_timeseries_dict
        context['get_requests_count'] = daily_resample_get.values.tolist()
        context['post_requests_count'] = daily_resample_posts.values.tolist()
        context['response_codes'] = response_code_dict

        return render(request, "accounts/staff_dashboard.html", context)

# Request logger view method:
class RequestLogViewSet(AbstractModelViewSet):
    """The REST API ViewSet for the 3rd party request logs. This viewset is only designed to return
    logging data, it does not perform any of the other CRUD functions associated with a REST API.
    It is designed explicitly for the purpose of being used by the Flask Logging system.
    """
    serializer_class = RequestSerializer
    queryset = Request.objects.all().order_by("time")
    
    def list(self, request):
        """This method reads monthly requesst logs, seralizes them and returns then in JSON
        format.
        """
        # Building the context that the method populateds:
        context = {}
        context["request"] = request

        # Extracting Query Params from the url:
        start_date = request.GET.get("Start-Date", None)
        end_date = request.GET.get("End-Date", None)
        user = request.GET.get("User", None)
        method = request.GET.get("Method", None)
        ip = request.GET.get("IP", None)
        
        # Filtering the query of Requests based on url query param:
        queryset = Request.objects.all().order_by("-time")

        # Date Time Filtering:
        if start_date is None and end_date is None:
            pass
        else:
            if end_date is None:
                queryset = queryset.filter(time__gt=start_date)

            if start_date is None:
                queryset = queryset.filter(time__lt=end_date)         

            if start_date and end_date is not None:
                queryset = queryset.filter(time__range=(start_date, end_date))
        pass
        
        # User filtering:
        if user is not None:
            queryset = queryset.filter(user=user)
        
        # IP address filtering:
        if ip is not None:
            queryset = queryset.filter(ip=ip)

        # Response type filtering:
        if method is not None:
            queryset = queryset.filter(method=method)

        # Creating the seralizer out of the queryset:
        seralizer = RequestSerializer(queryset, many=True, context=context)
        
        return Response(seralizer.data)

# Django Settings View Method:
class DjangoSettingsViewSet(AbstractModelViewSet):
    """This is the method that unpacks the Django settings that are currently
    being used by the project and displays them as a JSON. 

    The ViewSet only supports the reading section of a REST API, it does not allow
    the Django settings to be updated. This could be done through a simple view method
    as opposed to a full MVC ViewSet structure but a ViewSet is used to make use of the 
    user model permission system and token authentication functions.
    """
    queryset = Request.objects.all().order_by("time")
    serializer_class = SettingsSerializer

    def list(self, request):
        """Extracting all the relevant settings data and converting it to JSON.
        """
        # Extracting all non-critial settings:
        seralizer = SettingsSerializer(settings)

        # TODO: Manually unpack the settings module so that the seralizer can work with correct field types (DATABASE: DictField)

        return Response(seralizer.data)

# Ping view method:
def ping(request):
    """The method recives a request and returns a generic response that proves the server is
    online. This is a standard 'Ping-Pong' function and is used by loggers and microservices
    to quickly determine if the server is online.
    """
    return JsonResponse({
        "Response":"pong",
        "TimeStamp": time.time()
        })