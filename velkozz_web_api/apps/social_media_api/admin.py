# Importing Django Models:
from django.contrib import admin

# Importing Database Base Models:
from .models.reddit.reddit_models import RedditPosts
from .models.indeed.indeed_models import IndeedJobPosts
from .models.youtube.youtube_models import DailyYoutubeChannelStats

# Registering the Reddit Posts Model to Admin Dashboard:
admin.site.register(RedditPosts)

# Registering Indeed Models to Admin Dash:
admin.site.register(IndeedJobPosts)

# Registering Indeed Models to Admin Dash:
admin.site.register(DailyYoutubeChannelStats)
