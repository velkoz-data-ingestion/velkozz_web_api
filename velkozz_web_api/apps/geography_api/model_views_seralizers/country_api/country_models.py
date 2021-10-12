# Importing Django Database Packages:
from django.db import models
from django.contrib.postgres.fields import ArrayField

class Country(models.Model):
    """The database model for summary data about all countries extracted from 
    the REST Countries site.

    """
    common_name = models.CharField(max_length=70, primary_key=True, unique=True)
    names = models.JSONField()
    topLevelDomain = ArrayField(models.CharField(max_length=24), null=True)
    alpha2Code = models.CharField(max_length=2, null=True)
    numericCode = models.IntegerField(null=True)
    alpha3Code = models.CharField(max_length=3, null=True)
    cioc = models.CharField(max_length=3, null=True)
    independent = models.BooleanField(null=True)
    status = models.CharField(max_length=50, null=True)
    unMember = models.BooleanField(null=True)
    currencies = models.JSONField(null=True)
    callingCodes = models.JSONField(null=True)
    capital = models.CharField(max_length=65, null=True)
    altSpellings = ArrayField(models.CharField(max_length=150), null=True)
    region = models.CharField(max_length=100, null=True)
    subregion = models.CharField(max_length=100, null=True)
    languages = models.JSONField(null=True)
    translations = models.JSONField(null=True)
    latlng = ArrayField(models.FloatField(), null=True)
    landlocked = models.BooleanField(null=True)
    borders = ArrayField(models.CharField(max_length=3), null=True)
    area = models.FloatField(null=True)
    demonym = models.JSONField(null=True)

    def __str__(self):
        return self.common_name

    class Meta:
        verbose_name_plural = "Countries"
