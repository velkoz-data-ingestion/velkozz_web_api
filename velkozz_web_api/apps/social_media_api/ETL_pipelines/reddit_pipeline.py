# Importing reddit django models:
from social_media_api.model_views_seralizers.reddit_api.reddit_models import RedditDevApps, Subreddits, RedditLogs, RedditPosts

# Importing Scheduling Packages:
from apscheduler.schedulers.background import BackgroundScheduler

# Importing Reddit API:
import praw

# Import 3rd packages:
import time
from datetime import date, timedelta, datetime
import pytz


def load_reddit_data():
    """Method uses to PRAW api to extract top and hot posts from a specific subreddit and 
    write it to the database.
    """
    # Querying the reddit API credentials from the database:
    reddit_dev_app = RedditDevApps.objects.all().first()

    # Initalizing the reddit instance:
    reddit = praw.Reddit(
        client_id = reddit_dev_app.client_id,
        client_secret = reddit_dev_app.client_secret,
        user_agent = reddit_dev_app.user_agent
    )
    reddit.read_only = True

    # Querying a list of all sbureddits from the database:
    subreddits = [subreddit.search_name for subreddit in Subreddits.objects.all()]

    # Extracting and downloading top and hot daily posts from each subreddit:
    for subreddit in subreddits:
        
        # Creating subreddit instance:
        subreddit_instance = reddit.subreddit(subreddit)

        # Writing Top subreddit posts to database:
        top_posts = subreddit_instance.top("day", limit=25)
        hot_posts = subreddit_instance.hot(limit=25)

        # Unpacking the posts into a list to measure length for logging:
        top_posts_lst = [post for post in top_posts]
        hot_posts_lst = [post for post in hot_posts]

        def _format_datetime(utc_float):
            """Method ingests a utc timestamp float and formats it into
            a datetime format that is prefered by the DRF framework.
            It performs conversions through datetime and pytz.
            Args:
                utc (float): A unix timestamp.   
            Returns:
                str: The formatted datetime in string format.
            """
            date_obj = datetime.fromtimestamp(utc_float, tz=pytz.utc)
            date_str = date_obj.strftime("%Y-%m-%dT%H:%M:%S.%f%z")

            return date_str

        def write_posts(posts):
            """The method that ingests a list of subreddit posts made, trasnsforms the data into a
            format compatable with the database and then writes it to said database.
            
            In addition to writing data 

                - gold status
                - mod status
                - verified email status
                - the day the account was created
                - the comment karma of the account
                - the raw account name instead of a Redditor object.
            
            For each post in the list of posts a RedditPosts Django object is created and the data 
            is saved to the database.
            
            Arguments:
                posts (lst): A list of subreddit posts extracted via the praw API.

            """
            #print(posts)
            # Populating a dict with relevant post data:
            for post in posts:

                # Unpacking relevant author fields:
                author = post.author.name
                try:
                    author_gold = post.author.is_gold
                    mod_status = post.author.is_mod
                    verified_email_status = post.author.has_verified_email
                    acc_created_on = _format_datetime(post.author.created_utc)
                    comment_karma = post.author.comment_karma

                except Exception as e:
                    author_gold = None
                    mod_status = None
                    verified_email_status = None
                    acc_created_on = None
                    comment_karma = None

                # Creating the Reddit Post Object: 
                x = RedditPosts.objects.update_or_create(
                    id=post.id,
                    defaults = {
                        "id": post.id,
                        "subreddit": post.subreddit.display_name,
                        "title": post.title,
                        "content": post.selftext,
                        "upvote_ratio": post.upvote_ratio,
                        "score": post.score,
                        "num_comments": post.num_comments,
                        "created_on": _format_datetime(post.created_utc),
                        "stickied": post.stickied,
                        "over_18": post.over_18,
                        "spoiler":post.spoiler,
                        "author_is_gold":author_gold,
                        "author_mod":mod_status,
                        "author_has_verified_email":verified_email_status,
                        "permalink":post.permalink,
                        "author":post.author,
                        "author_created":acc_created_on,
                        "comment_karma":comment_karma               
                    }
                )

        # Loading all reddit posts to the database:
        try:
            write_posts(top_posts_lst)
            write_posts(hot_posts_lst)

            # Logging the Reddit Requests made:
            top_log = RedditLogs(subreddit=subreddit, fliter="top", num_posts=len(top_posts_lst), status_code=200)
            hot_log= RedditLogs(subreddit=subreddit, fliter="hot", num_posts=len(hot_posts_lst), status_code=200)
            top_log.save()
            hot_log.save()
            
        except Exception as e:
            # Logging the Reddit Requests made if ingestion does not work:
            top_log = RedditLogs(subreddit=subreddit, fliter="top", num_posts=len(top_posts_lst), status_code=400, error_msg=e)
            hot_log= RedditLogs(subreddit=subreddit, fliter="hot", num_posts=len(hot_posts_lst), status_code=400, error_msg=e)
            top_log.save()
            hot_log.save()

    time.sleep(5)

class RedditPipeline(object):
    """A method that is used to stop and start the reddit Background Scheduler. It is a class for state management.

    Args:
        test_status (Bool): Boolean indicating if the pipeline is running in test status.

        pipeline_active (Bool): Boolean determining/indicating if the pipeline is active or not.

        test_interval (int): The interval in minuites that the pipeline will be scheduled at when it is on
            test mode.

        prod_interval (int): The interval in hours tht the pipeline will be scheduled at when it is on production
            mode.

    """
    def __init__(self, test_status: bool, pipeline_active: bool, test_interval: int, prod_interval: int):
        self.scheduler = BackgroundScheduler()

        # Declaring instance variables:
        self.test_status = test_status
        self.pipeline_active = pipeline_active
        self.test_interval = test_interval
        self.prod_interval = prod_interval

        if self.test_status:
            self.scheduler.add_job(load_reddit_data, "interval", minutes=self.test_interval)
        else:
            self.scheduler.add_job(load_reddit_data, "interval", hours=self.prod_interval)

    def start_scheduler(self):
        self.scheduler.start()
        self.pipeline_active = True 
        
    def stop_scheduler(self):
        self.scheduler.stop()
        self.pipeline_active = False

