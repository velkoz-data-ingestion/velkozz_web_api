# Importing Django model methods:
from django.db import models
from django.contrib.postgres.fields import ArrayField

class NewsArticles(models.Model):
    """The django model that represents the contents of a news articles.

    It is built with the velkozz microservies in mind and is used as the 
    data structure that is seralized and served via the DRF REST API.

    Attributes:
        title (models.CharField): The title of the news article.
        
        authors (ArrayField): A list of people that have been listed as authors on the article.

        published_date (models.DateTimeField): The date that the article was uploaded by the source.

        article_text (models.TextField): The full body text of each article. This is the main content of each
            article extracted.

        meta_keywords (ArrayField): A list of keywords that are listed in the articles html source as
            meta-data.

        nlp_keywords (ArrayField): The keywords extracted from the main txt body via newspaper3k's nlp()
            extraction method. Unlike keywords it is extracted from the body of the text by an external process and
            is intended to be used for nlp processes.

        url (models.URLField): The original url for the article.

        source (models.CharField): The string representing the overarching source of the article. Eg: "CNN" or "BBC"

        timestamp (models.DateTimeField): The exact date time that the article was extracted via the microservice.
    
    """
    # Declaring model fields:
    # TODO: Change list fields back to array fields in prod once in PSQL:
    title = models.CharField(max_length=300, unique=True)
    #authors = ArrayField(base_field=models.CharField(max_length=150, blank=True))
    authors = models.TextField()
    meta_keywords = models.TextField()
    nlp_keywords = models.TextField()
    #meta_keywords = ArrayField(base_field=models.CharField(max_length=300, blank=True))
    #nlp_keywords = ArrayField(base_field=models.CharField(max_length=300, blank=True))
    published_date = models.DateField(null=True)
    article_text = models.TextField(null=True, blank=True)
    article_url = models.CharField(max_length=300)
    source = models.CharField(max_length=50)
    timestamp = models.DateTimeField()

    # String representation methods: 
    def __str__(self):
        return f"{self.source}-{self.title}-{self.published_date}"

    # Meta Config:
    class Meta: 
        verbose_name_plural = "News Articles"