from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('django-accounts/', include('django.contrib.auth.urls')),
    
    # Django REST API Authentication url:
    path("rest-auth/", include("rest_auth.urls")),
    
    # Routes for the main web core index urls:
    path("", include("accounts.urls")),
    
    # Routes for the Social Media API urls:
    path("social_media_api/", include("social_media_api.urls")),
    
    # Routes for the Finance Data API urls:
    path("finance_api/", include("finance_api.urls"))
]
