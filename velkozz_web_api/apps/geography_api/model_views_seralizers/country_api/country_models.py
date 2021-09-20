# Importing Django Database Packages:
from django.db import models
from django.contrib.postgres.fields import ArrayField

class Country(models.Model):
    """The database model for summary data about all countries extracted from 
    the REST Countries site.

    Attributes:
        name (models.CharField): The official name of the country.

        topLevelDomain (ArrayField): A list containing the url domain suffixes for the country.

        alpha2Code (models.CharField): The ISO two-letter country code.
        
        alpha3Code (models.CharField): the ISO three-letter country code.
        
        callingCodes (ArrayField): A list of telecom calling codes for the country.
        
        capital (models.CharField): The capital of the country.
        
        altSpellings (ArrayField): Potential alternate spellings for the country.
        
        region (models.CharField): The region the country is located in.
        
        subregion (models.CharField): The subregion the country is located in.
        
        population (models.IntegerField): The official population of the country.
        
        latlng (ArrayField): The latititude and longnitude coordinates of the country.
        
        demonym (models.CharField): The demonym for the people living in the country.
        
        area (models.FloatField): The size area of the country.
        
        gini (models.FloatField): The Gini Coefficent of the country.
        
        timezones (ArrayField): A list of official timezones for the country.
        
        borders (ArrayField): A list of the alpha 3 codes of countries that border the country.
        
        nativeName (models.CharField): How the country's name is represented in its native language.
        
        numericCode (models.IntegerField): The numeric code for the country.
        
        currencies (ArrayField): A list of the curriencies used in country. This list is made up of dicts that
            contain relevant information about each currency.
        
        languages (ArrayField): A list of official languages being used in country. Like currency data, this is a
            list of dicts that provide info on each language.
        
        translations (models.JSONField): A dict containing the name of the counry translated in main languages.
        
        reginalBlocs (ArrayField): A list of descriptive dicts about the geopolitical and economic blocks the 
            country is a part of. 
        
        cioc (models.CharField): The olympic regestration code for the counry. 
    """
    name = models.CharField(unique=True, primary_key=True, max_length=70)
    topLevelDomain = ArrayField(models.CharField(max_length=24))
    alpha2Code = models.CharField(max_length=2)
    alpha3Code = models.CharField(max_length=3)
    callingCodes = ArrayField(models.IntegerField())
    capital = models.CharField(max_length=20)
    altSpellings = ArrayField(models.CharField(max_length=150))
    region = models.CharField(max_length=100)
    subregion = models.CharField(max_length=100)
    population = models.IntegerField()
    latlng = ArrayField(models.FloatField())
    demonym = models.CharField(max_length=50)
    area = models.FloatField()
    gini = models.FloatField()
    timezones = ArrayField(models.CharField(max_length=150))
    borders = ArrayField(models.CharField(max_length=3))
    nativeName = models.CharField(max_length=100)
    numericCode = models.IntegerField()
    currencies = ArrayField(models.JSONField())
    languages = ArrayField(models.JSONField())
    translations = models.JSONField()
    regionalBlocs = ArrayField(models.JSONField())
    cioc = models.CharField(max_length=3)
