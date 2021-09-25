from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('django-accounts/', include('django.contrib.auth.urls')),
    
    # Django REST API Authentication url:
    path("rest-auth/", include("rest_auth.urls")),
    
    # Routes for the main web core index urls:
    path("", include("apps.accounts.urls")),
    
    # Routes for the Social Media API urls:
    path("social_media_api/", include("apps.social_media_api.urls")),
    
    # Routes for the Finance Data API urls:
    path("finance_api/", include("apps.finance_api.urls")),

    # Routes for the News Article Data API urls:
    path("news_api/", include("apps.news_api.urls")),

    # Routes for the Geography Data API urls:
    path("geography_api/", include("apps.geography_api.urls"))
]
