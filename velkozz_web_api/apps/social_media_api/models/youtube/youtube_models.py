# Importing Django database models: 
from django.db import models

# Base Youtube Channel Statistics 
class DailyYoutubeChannelStats(models.Model):
    """The Django database model for database table containing information
    about Youtube Channel view and subscriber statistics. 
    
    The model is meant to store data extracted about youtube channels via the 
    Google-Youtube API. It powers the DRF REST API for youtube channel views. 
    It is built for the velkozz API with the ETL pipeline API in mind. 

    The ETL API extract subreddit data in the tabular format:

    +------------+--------------+-------------+-------------------+--------------+----------------+
    | channel_id | channel_name | total_views | total_subscribers | total_videos | date_extracted |
    +------------+--------------+-------------+-------------------+--------------+----------------+
    |  string    |     int      |     int     |        int        |      int     |    datetime    |
    +------------+--------------+-------------+-------------------+--------------+----------------+

    References: 
        * https://developers.google.com/youtube/v3/docs/channels

    Attributes:

        channel_id (models.CharField): The google ID # used to identify a specific youtube
            channel. This is the ID that the Google API uses to extract channel statistics.

        channel_name (models.CharField): The dispalyed name of the channel. Used for user 
            identification of a channel.

        total_views (models.IntegerField): The total number of views the channel has across their entire
            catalogue. This value is used to calculate the number of views a channel gets per day. 

        total_subscribers (models.IntegerField): The total number of subscribers a channel has. Like 
            total channel views this is used to calculate the daily change in subscribers.

        total_videos (models.IntegerField): The total number of videos uploaded to the channel. 

        date_extracted (models.DateTimeField): The date time when the data was extracted from the youtube API.

    """
    channel_id = models.CharField(max_length=120)
    channel_name = models.CharField(max_length=100)
    total_views = models.IntegerField()
    total_subscribers = models.IntegerField()
    total_videos = models.IntegerField()
    date_extracted = models.DateTimeField(auto_now_add=True)    

    class Meta:
        verbose_name_plural = "Daily Youtube Channel Statistics"
        ordering = ['date_extracted']

    def __str__(self):
        return f"{self.channel_name}-{self.date_extracted}"