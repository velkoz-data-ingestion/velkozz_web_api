# Importing native django packages:
from django.db import models

class WallStreetBetsTickerMentions(models.Model):
    """
    Model represents the data table containing information about the
    counts of ticker symbol mentions from the subreddit wallstreetbets.

    The model is designed to store data from the format:

    {"TimeStamp": Counter()}

    eg: TDOD: Show example

    It stores the timestamp as a primary key and stores the dict value as a
    pickle byte string. 

    Attributes:
        day (models.DateTimeField): The day associated with the count of
            ticker mentions.

        ticker_count (models.TextField): The text field meant to store 
            the byte string of a JSON encoded collections.Counter dict.

    """
    day = models.DateField(primary_key=True, unique=True)
    ticker_count = models.TextField()

    class Meta:
        ordering = ['day']
        verbose_name_plural = "Wallstreetbets Ticker Mentions"