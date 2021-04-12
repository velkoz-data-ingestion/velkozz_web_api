# Importing Django Methods:
from django.urls import include, path
from rest_framework import routers
from rest_framework.authtoken import views

# Importing Account Views:
from .views import site_main_index, account_index, account_login, account_auth, api_docs, account_dashboard, account_create, staff_dash

# Importing App Configuration:
from social_media_api.apps import SocialMediaAPIConfig
from finance_api.apps import FinanceApiConfig

urlpatterns = [
    
    # Main Index of the Site:
    path("", site_main_index, name="main_index"),

    # Homepage for each user account:
    path("account", account_index, name="user_dashboard"),

    # User Account Dashboard Route:
    path("accout_dashboard", account_dashboard, name="user_account_dashboard"),

    # Authentication Routes:
    path(r"login/", account_login, name="login_page"),
    path(r"create_acc/", account_create, name="create_account_page"),
    path("accounts/auth/", account_auth, name="accountlogin"),
    path("api-token-auth/", views.obtain_auth_token),

    path("staff-dash/", staff_dash, name="staff_dashboard"),

    # Adding Routes for API Documentation:
    path("docs/<str:api_name>/", api_docs, name="api_docs")
]