# Importing Django Methods:
from django.urls import include, path
from rest_framework import routers

# Importing Account Views:
from .views import site_main_index, account_index, account_login, account_auth, api_docs
# Importing App Configuration:
from social_media_api.apps import SocialMediaAPIConfig
from finance_api.apps import FinanceApiConfig

urlpatterns = [
    
    # Main Index of the Site:
    path("", site_main_index, name="main_index"),

    # Index Homepage for each user account:
    path("account", account_index, name="user_dashboard"),

    # Authentication Routes:
    path(r"login/", account_login, name="login_page"),
    path("accounts/auth/", account_auth, name="accountlogin"),

    # Adding Routes for API Documentation:
    path("docs/<str:api_name>/", api_docs, name="api_docs")
]