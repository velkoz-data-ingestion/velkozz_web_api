from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # Django REST API Authentication:
    path("api-auth/", include('rest_framework.urls')),
    
    # Routes for the main web core index urls:
    path("", include("accounts.urls")),
    
    # Routes for the Social Media API urls:
    path("social_media_api/", include("social_media_api.urls")),
    
    # Routes for the Finance Data API urls:
    path("finance_api/", include("finance_api.urls"))
]
