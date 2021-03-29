# Importing Django Models:
from django.contrib import admin

# Importing Database Base Models:
from .models.reddit.reddit_models import RedditPosts

# All of the Subreddit model posts extended from RedditPosts:
reddit_db_models = RedditPosts.__subclasses__()

# Registering the Reddit Posts Models to the Admin Dashboard:
for reddit_model in reddit_db_models:
    admin.site.register(reddit_model)
