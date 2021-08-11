# Importing Django Methods:
from django.urls import include, path
from rest_framework import routers

# Importing the Reddit Views from the Reddit MVC:
from .model_views_seralizers.reddit_api import reddit_views
from .model_views_seralizers.indeed_api import indeed_views
from .model_views_seralizers.youtube_api import youtube_views

# Creating Url Router:
router = routers.DefaultRouter()

# Extracting a list of all ModelViewSet objects by extracting all the subclasses of parent object: 
subreddit_viewsets = reddit_views.RedditPostViewSet.__subclasses__()

# Iterating over each ModelViewSet dynamically registering routes to the router:
for viewset in subreddit_viewsets:
    router.register(fr"reddit/r{viewset.init_model.subreddit_name}", viewset)

# Adding endpoints for Indeed Job Listings:
router.register(r"jobs/indeed/listings", indeed_views.IndeedJobPostsViewSets)

# Adding endpoints for Youtube Data:
router.register(r"youtube/channel_daily", youtube_views.DailyYoutubeChannelStatsViewSet)

# Creating Automatic URL Routing:
urlpatterns = router.urls
    
