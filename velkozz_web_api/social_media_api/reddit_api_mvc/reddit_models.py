from django.db import models

# Reddit Data Pipeline Models:
class RedditPosts(models.Model):
    """A base model object that represents the data table
    for storing generic reddit posts from a single subreddit. 

    This model object is written as an abstract class to be inherited
    for other objects meant to represent specific subreddits. It is built
    for the velkozz API with the ETL pipeline API in mind. 

    The ETL API extract subreddit data in the tabular format:
    
    +----------+-------+-------+------------+-----+------------+----------+--------+-------+-------+---------+------+--------------+----------+-------------------------+--------------+-------------+
    |id (index)| title |content|upvote_ratio|score|num_comments|created_on|stickied|over_18|spoiler|permalink|author|author_is_gold|author_mod|author_has_verified_email|author_created|comment_karma|
    +----------+-------+-------+------------+-----+------------+----------+--------+-------+-------+---------+------+--------------+----------+-------------------------+--------------+-------------+
    | string   | string| string|   float    | int |     int    | datetime |  Bool  | Bool  |  Bool |   str   |  str |      Bool    |  Bool    |           Bool          |      str     |     int     |
    +----------+-------+-------+------------+-----+------------+----------+--------+-------+-------+---------+------+--------------+----------+-------------------------+--------------+-------------+

    Attributes:

        id (models.CharField): The unique reddit id for the post.

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
        primary_key=True,
        unique=True) 

    title = models.CharField(max_length= 300)
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


    permalink = models.URLField(
        max_length=300,
        null=True
    )

    author = models.CharField(max_length=300)
    author_created = models.DateTimeField()
    comment_karma = models.IntegerField(null=True)

    class Meta:
        abstract = True
        ordering = ['created_on']

    def __str__(self):
        return self.title

class WallStreetBetsPosts(RedditPosts):
    """The Model Method that represents the data table
    meant to store Reddit Posts from the subreddit 'r/wallstreetbets'.

    The model inherits from the RedditPosts abstract model class
    with the additional parameter 'subreddit' meant to indicate the subreddit
    that the post comes from.

    Attributes:

        subreddit (models.CharField): The name of the subreddit where the posts are
            extracted from. Default and Non-Editable the field is set to value "wallstreetbets".
    """
    subreddit = models.CharField(
        max_length=200,
        default="wallstreetbets",
        editable= False)

    class Meta:
        verbose_name_plural = "WallStreetBets Subreddit Posts"
        abstract = False
        ordering = ['created_on']

class SciencePosts(RedditPosts):
    """The Model Method that represents the data table
    meant to store Reddit Posts from the subreddit 'r/science'.

    The model inherits from the RedditPosts abstract model class
    with the additional parameter 'subreddit' meant to indicate the subreddit
    that the post comes from.

    Attributes:

        subreddit (models.CharField): The name of the subreddit where the posts are
            extracted from. Default and Non-Editable the field is set to value "science".
    """
    subreddit = models.CharField(
        max_length=200,
        default="science",
        editable= False)

    class Meta:
        verbose_name_plural = "Science Subreddit Posts"
        abstract = False
        ordering = ['created_on']
  