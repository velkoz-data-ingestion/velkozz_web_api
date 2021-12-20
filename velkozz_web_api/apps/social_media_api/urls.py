# Importing Django Methods:
from django.urls import include, path
from rest_framework import routers

# Importing the Reddit Views from the Reddit MVC:
from .model_views_seralizers.reddit_api import reddit_views
from .model_views_seralizers.indeed_api import indeed_views
from .model_views_seralizers.youtube_api import youtube_views

# Creating Url Router:
router = routers.DefaultRouter()

# Adding endpoint for Reddit Post API:
router.register(r"reddit/top_posts", reddit_views.RedditPostViewSet)
reddit_dashboard_path = path(r"reddit/dashboard", reddit_views.reddit_pipeline_dashboard, name="reddit_pipeline_dash")

# Adding endpoints for Indeed Job Listings:
router.register(r"jobs/indeed/listings", indeed_views.IndeedJobPostsViewSets)

# Adding endpoints for Youtube Data:
router.register(r"youtube/channel_daily", youtube_views.DailyYoutubeChannelStatsViewSet)

router.urls.append(reddit_dashboard_path)

# Creating Automatic URL Routing:
urlpatterns = router.urls 