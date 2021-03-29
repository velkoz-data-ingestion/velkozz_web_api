# Importing Django Modules:
from django.db import models

# Reddit Data Pipeline Model Template:
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
        primary_key=True) 

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


    permalink = models.CharField(
        max_length=300,
        null=True
    )

    author = models.CharField(max_length=300)
    author_created = models.DateTimeField()
    comment_karma = models.IntegerField(null=True)

    class Meta:
        abstract = True
        ordering = ['created_on']
        #default_permissions = ('add', 'change', 'delete', 'view')

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
    subreddit_name = "wallstreetbets"
    subreddit = models.CharField(
        max_length=200,
        default="wallstreetbets",
        editable= False)

    class Meta(RedditPosts.Meta):
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
    subreddit_name = "science"
    subreddit = models.CharField(
        max_length=200,
        default="science",
        editable= False)

    class Meta(RedditPosts.Meta):
        verbose_name_plural = "Science Subreddit Posts"
        abstract = False
        ordering = ['created_on']
  
class WorldNewsPosts(RedditPosts):
    """The Model Method that represents the data table
    meant to store Reddit Posts from the subreddit 'r/worldnews'.

    The model inherits from the RedditPosts abstract model class
    with the additional parameter 'subreddit' meant to indicate the subreddit
    that the post comes from.

    Attributes:

        subreddit (models.CharField): The name of the subreddit where the posts are
            extracted from. Default and Non-Editable the field is set to value of the subreddit name.
    """
    subreddit_name = "worldnews"
    subreddit = models.CharField(
        max_length=200,
        default="worldnews",
        editable= False)

    class Meta(RedditPosts.Meta):
        verbose_name_plural = "World News Subreddit Posts"
        abstract = False
        ordering = ['created_on']

class NewsPosts(RedditPosts):
    """The Model Method that represents the data table
    meant to store Reddit Posts from the subreddit 'r/news'.

    The model inherits from the RedditPosts abstract model class
    with the additional parameter 'subreddit' meant to indicate the subreddit
    that the post comes from.

    Attributes:

        subreddit (models.CharField): The name of the subreddit where the posts are
            extracted from. Default and Non-Editable the field is set to value of the subreddit name.
    """
    subreddit_name = "news"
    subreddit = models.CharField(
        max_length=200,
        default="news",
        editable= False)

    class Meta(RedditPosts.Meta):
        verbose_name_plural = "News Subreddit Posts"
        abstract = False
        ordering = ['created_on']

class EnergyPosts(RedditPosts):
    """The Model Method that represents the data table
    meant to store Reddit Posts from the subreddit 'r/energy'.

    The model inherits from the RedditPosts abstract model class
    with the additional parameter 'subreddit' meant to indicate the subreddit
    that the post comes from.

    Attributes:

        subreddit (models.CharField): The name of the subreddit where the posts are
            extracted from. Default and Non-Editable the field is set to value of the subreddit name.
    """
    subreddit_name = "energy"
    subreddit = models.CharField(
        max_length=200,
        default="energy",
        editable= False)

    class Meta(RedditPosts.Meta):
        verbose_name_plural = "Energy Subreddit Posts"
        abstract = False
        ordering = ['created_on']

class EconomicsPosts(RedditPosts):
    """The Model Method that represents the data table
    meant to store Reddit Posts from the subreddit 'r/Economics'.

    The model inherits from the RedditPosts abstract model class
    with the additional parameter 'subreddit' meant to indicate the subreddit
    that the post comes from.

    Attributes:

        subreddit (models.CharField): The name of the subreddit where the posts are
            extracted from. Default and Non-Editable the field is set to value of the subreddit name.
    """
    subreddit_name = "Economics"
    subreddit = models.CharField(
        max_length=200,
        default="Economics",
        editable= False)

    class Meta(RedditPosts.Meta):
        verbose_name_plural = "Economics Subreddit Posts"
        abstract = False
        ordering = ['created_on']

class PoliticsPosts(RedditPosts):
    """The Model Method that represents the data table
    meant to store Reddit Posts from the subreddit 'r/politics'.

    The model inherits from the RedditPosts abstract model class
    with the additional parameter 'subreddit' meant to indicate the subreddit
    that the post comes from.

    Attributes:

        subreddit (models.CharField): The name of the subreddit where the posts are
            extracted from. Default and Non-Editable the field is set to value of the subreddit name.
    """
    subreddit_name = "politics"
    subreddit = models.CharField(
        max_length=200,
        default="politics",
        editable= False)

    class Meta(RedditPosts.Meta):
        verbose_name_plural = "Politics Subreddit Posts"
        abstract = False
        ordering = ['created_on']

class CanadaPosts(RedditPosts):
    """The Model Method that represents the data table
    meant to store Reddit Posts from the subreddit 'r/canada'.

    The model inherits from the RedditPosts abstract model class
    with the additional parameter 'subreddit' meant to indicate the subreddit
    that the post comes from.

    Attributes:

        subreddit (models.CharField): The name of the subreddit where the posts are
            extracted from. Default and Non-Editable the field is set to value of the subreddit name.
    """
    subreddit_name = "canada"
    subreddit = models.CharField(
        max_length=200,
        default="canada",
        editable= False)

    class Meta(RedditPosts.Meta):
        verbose_name_plural = "Canada Subreddit Posts"
        abstract = False
        ordering = ['created_on']

class UKPoliticsPosts(RedditPosts):
    """The Model Method that represents the data table
    meant to store Reddit Posts from the subreddit 'r/ukpolitics'.

    The model inherits from the RedditPosts abstract model class
    with the additional parameter 'subreddit' meant to indicate the subreddit
    that the post comes from.

    Attributes:

        subreddit (models.CharField): The name of the subreddit where the posts are
            extracted from. Default and Non-Editable the field is set to value of the subreddit name.
    """
    subreddit_name = "ukpolitics"
    subreddit = models.CharField(
        max_length=200,
        default="ukpolitics",
        editable= False)

    class Meta(RedditPosts.Meta):
        verbose_name_plural = "UK Politics Subreddit Posts"
        abstract = False
        ordering = ['created_on']

class PalestinePosts(RedditPosts):
    """The Model Method that represents the data table
    meant to store Reddit Posts from the subreddit 'r/Palestine'.

    The model inherits from the RedditPosts abstract model class
    with the additional parameter 'subreddit' meant to indicate the subreddit
    that the post comes from.

    Attributes:

        subreddit (models.CharField): The name of the subreddit where the posts are
            extracted from. Default and Non-Editable the field is set to value of the subreddit name.
    """
    subreddit_name = "Palestine"
    subreddit = models.CharField(
        max_length=200,
        default="Palestine",
        editable= False)

    class Meta(RedditPosts.Meta):
        verbose_name_plural = "Palestine Subreddit Posts"
        abstract = False
        ordering = ['created_on']

class MiddleEastNewsPosts(RedditPosts):
    """The Model Method that represents the data table
    meant to store Reddit Posts from the subreddit 'r/MiddleEastNews'.

    The model inherits from the RedditPosts abstract model class
    with the additional parameter 'subreddit' meant to indicate the subreddit
    that the post comes from.

    Attributes:

        subreddit (models.CharField): The name of the subreddit where the posts are
            extracted from. Default and Non-Editable the field is set to value of the subreddit name.
    """
    subreddit_name = "MiddleEastNews"
    subreddit = models.CharField(
        max_length=200,
        default="MiddleEastNews",
        editable= False)

    class Meta(RedditPosts.Meta):
        verbose_name_plural = "MiddleEastNews Subreddit Posts"
        abstract = False
        ordering = ['created_on']

class IsraelPosts(RedditPosts):
    """The Model Method that represents the data table
    meant to store Reddit Posts from the subreddit 'r/Israel'.

    The model inherits from the RedditPosts abstract model class
    with the additional parameter 'subreddit' meant to indicate the subreddit
    that the post comes from.

    Attributes:

        subreddit (models.CharField): The name of the subreddit where the posts are
            extracted from. Default and Non-Editable the field is set to value of the subreddit name.
    """
    subreddit_name = "Israel"
    subreddit = models.CharField(
        max_length=200,
        default="Israel",
        editable= False)

    class Meta(RedditPosts.Meta):
        verbose_name_plural = "Israel Subreddit Posts"
        abstract = False
        ordering = ['created_on']

class PakistanPosts(RedditPosts):
    """The Model Method that represents the data table
    meant to store Reddit Posts from the subreddit 'r/pakistan'.

    The model inherits from the RedditPosts abstract model class
    with the additional parameter 'subreddit' meant to indicate the subreddit
    that the post comes from.

    Attributes:

        subreddit (models.CharField): The name of the subreddit where the posts are
            extracted from. Default and Non-Editable the field is set to value of the subreddit name.
    """
    subreddit_name = "pakistan"
    subreddit = models.CharField(
        max_length=200,
        default="pakistan",
        editable= False)

    class Meta(RedditPosts.Meta):
        verbose_name_plural = "Pakistan Subreddit Posts"
        abstract = False
        ordering = ['created_on']

class IndiaPosts(RedditPosts):
    """The Model Method that represents the data table
    meant to store Reddit Posts from the subreddit 'r/india'.

    The model inherits from the RedditPosts abstract model class
    with the additional parameter 'subreddit' meant to indicate the subreddit
    that the post comes from.

    Attributes:

        subreddit (models.CharField): The name of the subreddit where the posts are
            extracted from. Default and Non-Editable the field is set to value of the subreddit name.
    """
    subreddit_name = "india"
    subreddit = models.CharField(
        max_length=200,
        default="india",
        editable= False)

    class Meta(RedditPosts.Meta):
        verbose_name_plural = "India Subreddit Posts"
        abstract = False
        ordering = ['created_on']

class LibertarianPosts(RedditPosts):
    """The Model Method that represents the data table
    meant to store Reddit Posts from the subreddit 'r/Libertarian'.

    The model inherits from the RedditPosts abstract model class
    with the additional parameter 'subreddit' meant to indicate the subreddit
    that the post comes from.

    Attributes:

        subreddit (models.CharField): The name of the subreddit where the posts are
            extracted from. Default and Non-Editable the field is set to value of the subreddit name.
    """
    subreddit_name = "Libertarian"
    subreddit = models.CharField(
        max_length=200,
        default="Libertarian",
        editable= False)

    class Meta(RedditPosts.Meta):
        verbose_name_plural = "Libertarian Subreddit Posts"
        abstract = False
        ordering = ['created_on']

class ConservativePosts(RedditPosts):
    """The Model Method that represents the data table
    meant to store Reddit Posts from the subreddit 'r/Conservative'.

    The model inherits from the RedditPosts abstract model class
    with the additional parameter 'subreddit' meant to indicate the subreddit
    that the post comes from.

    Attributes:

        subreddit (models.CharField): The name of the subreddit where the posts are
            extracted from. Default and Non-Editable the field is set to value of the subreddit name.
    """
    subreddit_name = "Conservative"
    subreddit = models.CharField(
        max_length=200,
        default="Conservative",
        editable= False)

    class Meta(RedditPosts.Meta):
        verbose_name_plural = "Conservative Subreddit Posts"
        abstract = False
        ordering = ['created_on']

class SocialismPosts(RedditPosts):
    """The Model Method that represents the data table
    meant to store Reddit Posts from the subreddit 'r/socialism'.

    The model inherits from the RedditPosts abstract model class
    with the additional parameter 'subreddit' meant to indicate the subreddit
    that the post comes from.

    Attributes:

        subreddit (models.CharField): The name of the subreddit where the posts are
            extracted from. Default and Non-Editable the field is set to value of the subreddit name.
    """
    subreddit_name = "socialism"
    subreddit = models.CharField(
        max_length=200,
        default="socialism",
        editable= False)

    class Meta(RedditPosts.Meta):
        verbose_name_plural = "Socialism Subreddit Posts"
        abstract = False
        ordering = ['created_on']

class ProgressivePosts(RedditPosts): 
    """The Model Method that represents the data table
    meant to store Reddit Posts from the subreddit 'r/progressive'.

    The model inherits from the RedditPosts abstract model class
    with the additional parameter 'subreddit' meant to indicate the subreddit
    that the post comes from.

    Attributes:

        subreddit (models.CharField): The name of the subreddit where the posts are
            extracted from. Default and Non-Editable the field is set to value of the subreddit name.
    """
    subreddit_name = "progressive"
    subreddit = models.CharField(
        max_length=200,
        default="progressive",
        editable= False)

    class Meta(RedditPosts.Meta):
        verbose_name_plural = "Progressive Subreddit Posts"
        abstract = False
        ordering = ['created_on']

class DemocratsPosts(RedditPosts):
    """The Model Method that represents the data table
    meant to store Reddit Posts from the subreddit 'r/democrats'.

    The model inherits from the RedditPosts abstract model class
    with the additional parameter 'subreddit' meant to indicate the subreddit
    that the post comes from.

    Attributes:

        subreddit (models.CharField): The name of the subreddit where the posts are
            extracted from. Default and Non-Editable the field is set to value of the subreddit name.
    """
    subreddit_name = "democrats"
    subreddit = models.CharField(
        max_length=200,
        default="democrats",
        editable= False)

    class Meta(RedditPosts.Meta):
        verbose_name_plural = "Democrats Subreddit Posts"
        abstract = False
        ordering = ['created_on']

class LiberalPosts(RedditPosts):
    """The Model Method that represents the data table
    meant to store Reddit Posts from the subreddit 'r/Liberal'.

    The model inherits from the RedditPosts abstract model class
    with the additional parameter 'subreddit' meant to indicate the subreddit
    that the post comes from.

    Attributes:

        subreddit (models.CharField): The name of the subreddit where the posts are
            extracted from. Default and Non-Editable the field is set to value of the subreddit name.
    """
    subreddit_name = "Liberal"
    subreddit = models.CharField(
        max_length=200,
        default="Liberal",
        editable= False)

    class Meta(RedditPosts.Meta):
        verbose_name_plural = "Liberal Subreddit Posts"
        abstract = False
        ordering = ['created_on']

class TechnologyPosts(RedditPosts):
    """The Model Method that represents the data table
    meant to store Reddit Posts from the subreddit 'r/technology'.

    The model inherits from the RedditPosts abstract model class
    with the additional parameter 'subreddit' meant to indicate the subreddit
    that the post comes from.

    Attributes:

        subreddit (models.CharField): The name of the subreddit where the posts are
            extracted from. Default and Non-Editable the field is set to value of the subreddit name.
    """
    subreddit_name = "technology"
    subreddit = models.CharField(
        max_length=200,
        default="technology",
        editable= False)

    class Meta(RedditPosts.Meta):
        verbose_name_plural = "Technology Subreddit Posts"
        abstract = False
        ordering = ['created_on']

class RealTechPosts(RedditPosts):
    """The Model Method that represents the data table
    meant to store Reddit Posts from the subreddit 'r/realtech'.

    The model inherits from the RedditPosts abstract model class
    with the additional parameter 'subreddit' meant to indicate the subreddit
    that the post comes from.

    Attributes:

        subreddit (models.CharField): The name of the subreddit where the posts are
            extracted from. Default and Non-Editable the field is set to value of the subreddit name.
    """
    subreddit_name = "realtech"
    subreddit = models.CharField(
        max_length=200,
        default="realtech",
        editable= False)

    class Meta(RedditPosts.Meta):
        verbose_name_plural = "Realtech Subreddit Posts"
        abstract = False
        ordering = ['created_on']

class TechPosts(RedditPosts):
    """The Model Method that represents the data table
    meant to store Reddit Posts from the subreddit 'r/tech'.

    The model inherits from the RedditPosts abstract model class
    with the additional parameter 'subreddit' meant to indicate the subreddit
    that the post comes from.

    Attributes:

        subreddit (models.CharField): The name of the subreddit where the posts are
            extracted from. Default and Non-Editable the field is set to value of the subreddit name.
    """
    subreddit_name = "tech"
    subreddit = models.CharField(
        max_length=200,
        default="tech",
        editable= False)

    class Meta(RedditPosts.Meta):
        verbose_name_plural = "Tech Subreddit Posts"
        abstract = False
        ordering = ['created_on']

class NeutralPoliticsPosts(RedditPosts):
    """The Model Method that represents the data table
    meant to store Reddit Posts from the subreddit 'r/NeutralPolitics'.

    The model inherits from the RedditPosts abstract model class
    with the additional parameter 'subreddit' meant to indicate the subreddit
    that the post comes from.

    Attributes:

        subreddit (models.CharField): The name of the subreddit where the posts are
            extracted from. Default and Non-Editable the field is set to value of the subreddit name.
    """
    subreddit_name = "NeutralPolitics"
    subreddit = models.CharField(
        max_length=200,
        default="NeutralPolitics",
        editable= False)

    class Meta(RedditPosts.Meta):
        verbose_name_plural = "NeutralPolitics Subreddit Posts"
        abstract = False
        ordering = ['created_on']

class ChinaPosts(RedditPosts):
    """The Model Method that represents the data table
    meant to store Reddit Posts from the subreddit 'r/China'.

    The model inherits from the RedditPosts abstract model class
    with the additional parameter 'subreddit' meant to indicate the subreddit
    that the post comes from.

    Attributes:

        subreddit (models.CharField): The name of the subreddit where the posts are
            extracted from. Default and Non-Editable the field is set to value of the subreddit name.
    """
    subreddit_name = "China"
    subreddit = models.CharField(
        max_length=200,
        default="China",
        editable= False)

    class Meta(RedditPosts.Meta):
        verbose_name_plural = "China Subreddit Posts"
        abstract = False
        ordering = ['created_on']

class TaiwanPosts(RedditPosts):
    """The Model Method that represents the data table
    meant to store Reddit Posts from the subreddit 'r/taiwan'.

    The model inherits from the RedditPosts abstract model class
    with the additional parameter 'subreddit' meant to indicate the subreddit
    that the post comes from.

    Attributes:

        subreddit (models.CharField): The name of the subreddit where the posts are
            extracted from. Default and Non-Editable the field is set to value of the subreddit name.
    """
    subreddit_name = "taiwan"
    subreddit = models.CharField(
        max_length=200,
        default="taiwan",
        editable= False)

    class Meta(RedditPosts.Meta):
        verbose_name_plural = "Taiwan Subreddit Posts"
        abstract = False
        ordering = ['created_on']

class JapanPosts(RedditPosts):
    """The Model Method that represents the data table
    meant to store Reddit Posts from the subreddit 'r/japan'.

    The model inherits from the RedditPosts abstract model class
    with the additional parameter 'subreddit' meant to indicate the subreddit
    that the post comes from.

    Attributes:

        subreddit (models.CharField): The name of the subreddit where the posts are
            extracted from. Default and Non-Editable the field is set to value of the subreddit name.
    """
    subreddit_name = "japan"
    subreddit = models.CharField(
        max_length=200,
        default="japan",
        editable= False)

    class Meta(RedditPosts.Meta):
        verbose_name_plural = "Japan Subreddit Posts"
        abstract = False
        ordering = ['created_on']

class KoreaPosts(RedditPosts):
    """The Model Method that represents the data table
    meant to store Reddit Posts from the subreddit 'r/korea'.

    The model inherits from the RedditPosts abstract model class
    with the additional parameter 'subreddit' meant to indicate the subreddit
    that the post comes from.

    Attributes:

        subreddit (models.CharField): The name of the subreddit where the posts are
            extracted from. Default and Non-Editable the field is set to value of the subreddit name.
    """
    subreddit_name = "korea"
    subreddit = models.CharField(
        max_length=200,
        default="korea",
        editable= False)

    class Meta(RedditPosts.Meta):
        verbose_name_plural = "Korea Subreddit Posts"
        abstract = False
        ordering = ['created_on']

class SingaporePosts(RedditPosts):
    """The Model Method that represents the data table
    meant to store Reddit Posts from the subreddit 'r/singapore'.

    The model inherits from the RedditPosts abstract model class
    with the additional parameter 'subreddit' meant to indicate the subreddit
    that the post comes from.

    Attributes:

        subreddit (models.CharField): The name of the subreddit where the posts are
            extracted from. Default and Non-Editable the field is set to value of the subreddit name.
    """
    subreddit_name = "singapore"
    subreddit = models.CharField(
        max_length=200,
        default="singapore",
        editable= False)

    class Meta(RedditPosts.Meta):
        verbose_name_plural = "Singapore Subreddit Posts"
        abstract = False
        ordering = ['created_on']

class MalaysiaPosts(RedditPosts):
    """The Model Method that represents the data table
    meant to store Reddit Posts from the subreddit 'r/malaysia'.

    The model inherits from the RedditPosts abstract model class
    with the additional parameter 'subreddit' meant to indicate the subreddit
    that the post comes from.

    Attributes:

        subreddit (models.CharField): The name of the subreddit where the posts are
            extracted from. Default and Non-Editable the field is set to value of the subreddit name.
    """
    subreddit_name = "malaysia"
    subreddit = models.CharField(
        max_length=200,
        default="malaysia",
        editable= False)

    class Meta(RedditPosts.Meta):
        verbose_name_plural = "Malaysia Subreddit Posts"
        abstract = False
        ordering = ['created_on']

class ThailandPosts(RedditPosts):
    """The Model Method that represents the data table
    meant to store Reddit Posts from the subreddit 'r/Thailand'.

    The model inherits from the RedditPosts abstract model class
    with the additional parameter 'subreddit' meant to indicate the subreddit
    that the post comes from.

    Attributes:

        subreddit (models.CharField): The name of the subreddit where the posts are
            extracted from. Default and Non-Editable the field is set to value of the subreddit name.
    """
    subreddit_name = "Thailand"
    subreddit = models.CharField(
        max_length=200,
        default="Thailand",
        editable= False)

    class Meta(RedditPosts.Meta):
        verbose_name_plural = "Thailand Subreddit Posts"
        abstract = False
        ordering = ['created_on']
        
class NorthKoreaPosts(RedditPosts):
    """The Model Method that represents the data table
    meant to store Reddit Posts from the subreddit 'r/northkorea'.

    The model inherits from the RedditPosts abstract model class
    with the additional parameter 'subreddit' meant to indicate the subreddit
    that the post comes from.

    Attributes:

        subreddit (models.CharField): The name of the subreddit where the posts are
            extracted from. Default and Non-Editable the field is set to value of the subreddit name.
    """
    subreddit_name = "northkorea"
    subreddit = models.CharField(
        max_length=200,
        default="northkorea",
        editable= False)

    class Meta(RedditPosts.Meta):
        verbose_name_plural = "North Korea Subreddit Posts"
        abstract = False
        ordering = ['created_on']

class NorthKoreaNewsPosts(RedditPosts):
    """The Model Method that represents the data table
    meant to store Reddit Posts from the subreddit 'r/NorthKoreaNews'.

    The model inherits from the RedditPosts abstract model class
    with the additional parameter 'subreddit' meant to indicate the subreddit
    that the post comes from.

    Attributes:

        subreddit (models.CharField): The name of the subreddit where the posts are
            extracted from. Default and Non-Editable the field is set to value of the subreddit name.
    """
    subreddit_name = "NorthKoreaNews"
    subreddit = models.CharField(
        max_length=200,
        default="NorthKoreaNews",
        editable= False)

    class Meta(RedditPosts.Meta):
        verbose_name_plural = "NorthKoreaNews Subreddit Posts"
        abstract = False
        ordering = ['created_on']

class ConflictNewsPosts(RedditPosts):
    """The Model Method that represents the data table
    meant to store Reddit Posts from the subreddit 'r/ConflictNews'.

    The model inherits from the RedditPosts abstract model class
    with the additional parameter 'subreddit' meant to indicate the subreddit
    that the post comes from.

    Attributes:

        subreddit (models.CharField): The name of the subreddit where the posts are
            extracted from. Default and Non-Editable the field is set to value of the subreddit name.
    """
    subreddit_name = "ConflictNews"
    subreddit = models.CharField(
        max_length=200,
        default="ConflictNews",
        editable= False)

    class Meta(RedditPosts.Meta):
        verbose_name_plural = "ConflictNews Subreddit Posts"
        abstract = False
        ordering = ['created_on']

class HongKongPosts(RedditPosts):
    """The Model Method that represents the data table
    meant to store Reddit Posts from the subreddit 'r/HongKong'.

    The model inherits from the RedditPosts abstract model class
    with the additional parameter 'subreddit' meant to indicate the subreddit
    that the post comes from.

    Attributes:

        subreddit (models.CharField): The name of the subreddit where the posts are
            extracted from. Default and Non-Editable the field is set to value of the subreddit name.
    """
    subreddit_name = "HongKong"
    subreddit = models.CharField(
        max_length=200,
        default="HongKong",
        editable= False)

    class Meta(RedditPosts.Meta):
        verbose_name_plural = "HongKong Subreddit Posts"
        abstract = False
        ordering = ['created_on']

class SpacePosts(RedditPosts):
    """The Model Method that represents the data table
    meant to store Reddit Posts from the subreddit 'r/space'.

    The model inherits from the RedditPosts abstract model class
    with the additional parameter 'subreddit' meant to indicate the subreddit
    that the post comes from.

    Attributes:

        subreddit (models.CharField): The name of the subreddit where the posts are
            extracted from. Default and Non-Editable the field is set to value of the subreddit name.
    """
    subreddit_name = "space"
    subreddit = models.CharField(
        max_length=200,
        default="HongKong",
        editable= False)

    class Meta(RedditPosts.Meta):
        verbose_name_plural = "Space Subreddit Posts"
        abstract = False
        ordering = ['created_on']

class CryptoCurrencyPosts(RedditPosts):
    """The Model Method that represents the data table
    meant to store Reddit Posts from the subreddit 'r/CryptoCurrency'.

    The model inherits from the RedditPosts abstract model class
    with the additional parameter 'subreddit' meant to indicate the subreddit
    that the post comes from.

    Attributes:

        subreddit (models.CharField): The name of the subreddit where the posts are
            extracted from. Default and Non-Editable the field is set to value of the subreddit name.
    """
    subreddit_name = "CryptoCurrency"
    subreddit = models.CharField(
        max_length=200,
        default="HongKong",
        editable= False)

    class Meta(RedditPosts.Meta):
        verbose_name_plural = "CryptoCurrency Subreddit Posts"
        abstract = False
        ordering = ['created_on']

# Method that extracts a list of subreddits from a parent Model:
def get_subreddit_lst(parent_model):
    """A method that ingests a parent django model and extracts
    a list of 'subreddit_name' params for the parent model's 
    subclasses.

    Args:
        parent_model (django.db.models.Model): The parent model
            for subreddit posts called RedditPosts
    
    Return: 
        lst: The list of strings representing the subreddt names
            for all parent_method subclasses.
    
    """
    # Extracting list of subreddit names via comprehension:
    subreddit_name_lst = [
        subclass.subreddit_name for subclass in parent_model.__subclasses__() 
        ]

    return subreddit_name_lst