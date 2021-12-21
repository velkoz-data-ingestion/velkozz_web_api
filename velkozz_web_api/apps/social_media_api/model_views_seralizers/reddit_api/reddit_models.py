# Importing Django Modules:
from django.db import models
from django.forms import ModelForm, PasswordInput

# Importing Scheduling Packages:
from apscheduler.schedulers.background import BackgroundScheduler

# Importing Reddit API:
import praw

# Import 3rd packages:
import time
from datetime import date, timedelta, datetime
import pytz

# TODO: Add event listener to Background Scheduelr to log database stuff for the actual scheduler.
# BackgroundScheduler.add_listener()

# Model for Reddit Developr API: 
class RedditDevApps(models.Model):
    """The database model containing the developer information for Reddits Developer API.

    It is used to authenticate PRAW for the web scrapers. The database model is designed to 
    maintain and run reddit ETL pipelines that are attached to the Developer Apps. This database
    model is designed to only have one entry.

    The main pipeline for ingesting reddit posts are managed by changes in the RedditPipeline model.

    Attributes:
        application_name (models.CharField): The name of the developer application.
    
        client_id (models.CharField): The 14 character string representing the reddit developer application.

        client_secret (models.CharField): A 27-character string secret key for the specific application.

        user_agent (models.CharField): The description of the reddit application used for application only flow of PRAW auth.

    """
    # Configuration of the Reddit Dev Account:
    application_name = models.CharField(max_length=25)
    client_id = models.CharField(max_length=35)
    client_secret = models.CharField(max_length=50)
    user_agent = models.CharField(max_length=100)
    
    class Meta:
        verbose_name_plural = "Reddit Developer Applications"
        abstract = False

    def __str__(self):
        return self.application_name

# Model for the Reddit Pipeline:
class RedditPipeline(models.Model):
    """A database model that represents the Reddit ETL Pipeline. A single insance of this object is created and
    it is used to toggle the Reddit ETL Pipeline on and off based on the modification of the model fields.

    This is done by attaching the Pipeline logic to the save() method of the model, allowing the Background Schdeuler
    to be modified everytime a config field is saved.

    Attributes:
        pipeline_active (models.BooleanField): A boolean that activates or deactivates the reddit ETL pipeline.

        pipeline_test_status (models.BooleanField): A boolean field indicating if the pipeline is started in test mode or not.

        test_interval (models.IntegerField): The interval in minuites that the pipeline will be scheduled at when it is on
            test mode.
        
        prod_interval (models.IntegerField): The interval in hours tht the pipeline will be scheduled at when it is on production
            mode.

        active_modified (models.DateTimeField): field indicating the last time any key parameter was changed regarding the activation
            status of the pipeline.
            
    """
    # Background Scheduler status:
    pipeline_active = models.BooleanField(default=False)
    active_modified = models.DateTimeField(auto_now=True)
    pipeline_test_status = models.BooleanField(default=True)
    
    # Background Scheduler Interval:
    test_interval = models.IntegerField(default=2)
    prod_interval = models.IntegerField(default=12)

    def save(self, *args, **kwargs):
        """Overwriting the default save method so that when changes are made to the model fields these
        changes are reflected in changes in the Pipeline object.
        
        The save method saves all the changes to the fields in the database and then creates a RedditPipeline
        object using said model fields that are used to ingest reddit data in the background.
        """
        # Querying the RedditDevApps model to enusre that Reddit Dev Credentials exist:
        reddit_dev_apps = RedditDevApps.objects.all().first()

        # If Reddit Dev Creds exists, initalizing pipeline: 
        if reddit_dev_apps != None:
            # Executing dafault save method:
            super().save(*args, **kwargs)

            # Creating Reddit Object Instance:
            reddit_pipeline = self.RedditPipelineScheduler(
                test_status=self.pipeline_test_status,
                pipeline_active=self.pipeline_active,
                test_interval=self.test_interval,
                prod_interval=self.prod_interval
            )

            # Activating the reddit pipeline based on the new params:
            if self.pipeline_active:
                reddit_pipeline.start_scheduler()

            else:
                pass
        
        # If there is no Reddit Dev Application then not performing the save() function as there is no 
        # propose for creating a RedditPipeline instance. 
        else:
            pass

    # Reddit ETL Logic:
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
                top_log = RedditLogs(subreddit=subreddit, subreddit_filter="top", num_posts=len(top_posts_lst), status_code=200)
                hot_log= RedditLogs(subreddit=subreddit, subreddit_filter="hot", num_posts=len(hot_posts_lst), status_code=200)
                top_log.save()
                hot_log.save()
                
            except Exception as e:
                # Logging the Reddit Requests made if ingestion does not work:
                top_log = RedditLogs(subreddit=subreddit, subreddit_filter="top", num_posts=len(top_posts_lst), status_code=400, error_msg=e)
                hot_log= RedditLogs(subreddit=subreddit, subreddit_filter="hot", num_posts=len(hot_posts_lst), status_code=400, error_msg=e)
                top_log.save()
                hot_log.save()

        time.sleep(5)

    # Reddit ETL Pipeline Object w/ Backround Scheduler:
    class RedditPipelineScheduler:
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
                self.scheduler.add_job(RedditPipeline.load_reddit_data, "interval", minutes=self.test_interval)
            else:
                self.scheduler.add_job(RedditPipeline.load_reddit_data, "interval", hours=self.prod_interval)

        def start_scheduler(self):
            self.scheduler.start()
            self.pipeline_active = True 
            
        def stop_scheduler(self):
            self.scheduler.remove()
            self.pipeline_active = False

    class Meta:
        abstract = False
        verbose_name_plural = "Reddit ETL Pipeline"

# Form associated with the Reddit Developer Application:
class RedditDevAppForm(ModelForm):
    """The Form for the model RedditDevApps, included here to include password fields.
    """
    class Meta:
        model = RedditDevApps
        fields = "__all__"
        widgets = {
            "client_secret": PasswordInput(),
        }

# Reddit Data Pipeline Model:
class RedditPosts(models.Model):
    """A django model object that represents the data table
    for reddit posts.
    
    It is built for the velkozz API with the ETL pipeline API in mind.
    This is the only table that stores reddit post data for every subreddit.
    subreddit-specific data is seperated out during data queries as opposed to
    during ingestion.

    The ETL API extract subreddit data in the tabular format:
    
    +----------+---------+-------+-------+------------+-----+------------+----------+--------+-------+-------+---------+------+--------------+----------+-------------------------+--------------+-------------+
    |id (index)|subreddit| title |content|upvote_ratio|score|num_comments|created_on|stickied|over_18|spoiler|permalink|author|author_is_gold|author_mod|author_has_verified_email|author_created|comment_karma|
    +----------+---------+-------+-------+------------+-----+------------+----------+--------+-------+-------+---------+------+--------------+----------+-------------------------+--------------+-------------+
    | string   | string  |string | string|   float    | int |     int    | datetime |  Bool  | Bool  |  Bool |   str   |  str |      Bool    |  Bool    |           Bool          |      str     |     int     |
    +----------+---------+-------+-------+------------+-----+------------+----------+--------+-------+-------+---------+------+--------------+----------+-------------------------+--------------+-------------+

    Attributes:

        id (models.CharField): The unique reddit id for the post.

        subreddit (models.CharField): The name of the subreddit of the post.

        title (models.CharField): The title of the reddit post.
        
        content (models.TextField): The full text content of the reddit post in markdown format.
        
        upvote_ratio (models.FloatField): The ratio of upvotes to downvotes of the post.
        
        score (models.IntegerField): The number of upvotes the post has.
        
        num_comments (models.IntegerField): The number of comments the post has.
        
        created_on (models.DateTimeField): The Date and Time the post was created in UTC.
        
        stickied (models.BooleanField): A Boolean indicating if the post was "stuck" or 
            "pinned" to the top of the subreddit.

        over_18 (models.BooleanField): A Boolean indicating if the post is marked Not Safe For Work.

        spoiler (models.Boolean): A Boolean indicating if the post is marked as a spoiler.

        permalink (models.CharField): The permanent url path to the post.

        author (models.CharField): The name of the author of the post.

        author_is_gold: (models.IntegerField): A Boolean indicating if the author of the post has been given gold. 

        author_mod: (models.BooleanField): A Boolean, indicating if the author
            of the post is a moderator of the subreddit. 

        author_has_verified_email: (models.BooleanField): A Boolean Field indicating if the author
            of the post has a verified email. 

        author_created (models.DateTimeField): The UTC date and time that the author's account was created.

        comment_karma (models.IntegerField): The amount of karma that a post has.

    """
    id = models.CharField(
        max_length=20,
        db_index= True,
        primary_key=True) 
    
    title = models.CharField(max_length= 300, null=True)
    subreddit = models.CharField(max_length=200, null=True)
    content = models.TextField(null=True)
    upvote_ratio = models.FloatField(null=True)
    score = models.IntegerField(null=True)
    num_comments = models.IntegerField(null=True)
    created_on = models.DateTimeField()

    # Boolean Fields:
    stickied = models.BooleanField(null=True)
    over_18 = models.BooleanField(null=True)
    spoiler = models.BooleanField(null=True)
    author_is_gold = models.BooleanField(null=True)
    author_mod = models.BooleanField(null=True)
    author_has_verified_email = models.BooleanField(null=True)


    permalink = models.CharField(
        max_length=300,
        null=True
    )

    author = models.CharField(max_length=300, null=True)
    author_created = models.DateTimeField(null=True)
    comment_karma = models.IntegerField(null=True)

    class Meta:
        verbose_name_plural = "Reddit Posts"
        abstract = False
        ordering = ['created_on']
        #default_permissions = ('add', 'change', 'delete', 'view')

    def __str__(self):
        return f"{self.title}-{self.subreddit}"

# Model for a list of subreddits:
class Subreddits(models.Model):
    """A model for a list of subreddits that are of importance to the reddit ETL.

    Attributes:
        subreddit_name (models.CharField): The human readable name of the subreddit.

        description (models.CharField): The description of the subreddit found on its homepage.

        search_name (models.CharField): The machine readable name of the subreddit used for querying the API. eg: redditdev
    """
    subreddit_name = models.CharField(max_length=50)
    description = models.CharField(max_length=200, null=True)
    search_name = models.CharField(max_length=50)

    def __str__(self):
        return self.subreddit_name

    class Meta:
        verbose_name_plural = "Subreddits"
        abstract = False
        ordering = ['subreddit_name']

# Reddit Logging Model:
class RedditLogs(models.Model):
    """
    Attributes:
        subreddit (models.CharField): The name of the subreddit where the posts were extracted from.

        subreddit_filter (models.CharField): The filter applied to the subreddit search to get the post (eg: top, hot).

        extracted_on (models.DateTimeField): The datetime that the request was made to reddit throught the PRAW API.

        num_posts (models.IntegerField): The number of posts that were extracted with the PRAW call.

        status_code (models.IntegerField): A status code that indicates if the log contains an error or not. (200 is good). 

        error_msg (models.CharField): The error message if the log contains one. If there is no error the value is null.

    """
    subreddit = models.CharField(max_length=50)
    subreddit_filter = models.CharField(max_length=10)
    extracted_on = models.DateTimeField(auto_now=True)
    num_posts = models.IntegerField()
    status_code = models.IntegerField()
    error_msg = models.CharField(max_length=200, null=True)

    def __str__(self):
        return f"{self.subreddit}-{self.num_posts}-{self.extracted_on}"

    class Meta:
        verbose_name_plural = "Reddit ETL Logs"
        abstract = False
        ordering = ['extracted_on']
