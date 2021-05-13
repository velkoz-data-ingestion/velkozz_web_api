# Importing django models: 
from django.db import models


# Model for indeed job posts:
class IndeedJobPosts(models.Model):
    """A database model containing the fields for storing data about
    job listings extracted from indeed.com.

    Attributes:

        id (models.CharField): The unique identifier for a job listing from indeed. Each id is
            unique to each job posting listed on the indeed website.

        title (models.CharField): The title of the indeed job listing. 

        company (models.CharField): The company making the job posting.

        location (models.CharField): The location of the job listing. Its maximum granularity is
            the city of the listing.

        summary (models.TextField): A short/medium length summary of the job listing made by the
            company.

        date_posted (models.DateField): The date that the job listing was posted.

    """
    id = models.CharField(unique=True, max_length=100, primary_key=True)
    title = models.CharField(max_length=300)
    company = models.CharField(max_length=200)
    location = models.CharField(max_length=200)
    summary = models.TextField(null=True)
    date_posted = models.DateField()

    def __str__(self):
        return f"{self.title}-{self.id}"

    class Meta:
        verbose_name_plural = "Indeed Job Posts"