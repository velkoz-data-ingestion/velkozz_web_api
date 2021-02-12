# Importing Django Methods:
from django.urls import include, path
from rest_framework import routers

# Importing Account Views:
from .views import site_main_index, account_index

urlpatterns = [
    
    # Main Index of the Site:
    path("", site_main_index, name="main_index"),

    # Index Homepage for each user account:
    path("account", account_index, name="user_dashboard")
]