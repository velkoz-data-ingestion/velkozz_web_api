# Importing Django Methods:
from django.urls import include, path
from rest_framework import routers

# Importing Account Views:
from .views import site_main_index, account_index, social_media_docs, finance_docs

# Importing App Configuration:
from social_media_api.apps import SocialMediaAPIConfig
from finance_api.apps import FinanceApiConfig

urlpatterns = [
    
    # Main Index of the Site:
    path("", site_main_index, name="main_index"),

    # Index Homepage for each user account:
    path("account", account_index, name="user_dashboard"),

    # Adding Routes for API Documentation:
    path("docs/social_media_api", social_media_docs, name=SocialMediaAPIConfig.name),
    path("docs/finance_data_api", finance_docs, name=FinanceApiConfig.name)
]