# Importing Django Models:
from django.contrib import admin

# Importing Database Base Models:
from social_media_api.model_views_seralizers.reddit_api.reddit_models import RedditPosts, RedditDevApps, RedditDevAppForm, Subreddits, RedditLogs
from .models.indeed.indeed_models import IndeedJobPosts
from .models.youtube.youtube_models import DailyYoutubeChannelStats

"<----------Reddit ETL Admin Models---------->"
# Creating an admin form for Reddit Developer Applications:
class RedditDevAppAdmin(admin.ModelAdmin):
    # Custom form for secret key pswrd:
    form = RedditDevAppForm 

    # Preventing the creation of more than one entry (we only need one Dev App):
    def has_add_permission(self, request):
        count = RedditDevApps.objects.all().count()
        if count == 0:
            return True
        return False

# Registering the Reddit ETL Models to Admin Dashboard:
admin.site.register(Subreddits)
admin.site.register(RedditPosts)
admin.site.register(RedditDevApps, RedditDevAppAdmin)
admin.site.register(RedditLogs)

# Registering Indeed Models to Admin Dash:
admin.site.register(IndeedJobPosts)

# Registering Indeed Models to Admin Dash:
admin.site.register(DailyYoutubeChannelStats)
