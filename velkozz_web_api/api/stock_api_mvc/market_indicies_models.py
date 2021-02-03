# Importing django models:
from django.db import models

# Creating Database models for Market Indicies:

# The SPY 500 Index Composition:
class SPYIndexComposition(models.Model):
    """A data model representing a database table containing information
    on the S&P500 market index composition. 

    It is built for the velkozz API with the ETL pipeline API in mind for POST
    requsts. There is no primary key declared, the model makes use of django's 
    automatic primary key pk. 

    Attributes:

        symbol (models.CharField): The ticker symbol of the stock in the index.

        security_name (models.CharField): The full name of the stock in the index.

        gics_sector (models.CharField): The Global Industry Classification Standard 
            category that the stock belongs to.

        gics_sub_industry (models.CharField): The Global Industry Classification Standard
            sub industry category that the stock belongs to.
        
        headquarters_location (models.CharField): The city where the company's headquarters 
            are located.
        
        date_added (models.DateTimeField): The date that the stock was added to the index. 

        cik (models.IntegerField): The SEC CIK identification number for the stock.

        founded (models.CharField): The year that the company was founded.

    """
    symbol = models.CharField(max_length=10, unique=True)
    security_name = models.CharField(max_length=100, unique=True)
    gics_sector = models.CharField(max_length=100, null=True)
    gics_sub_industry = models.CharField(max_length=100, null=True)
    headquarters_location = models.CharField(max_length=100, null=True)
    date_added = models.DateField()
    cik = models.IntegerField(max_length=20, unique=True)
    founded = models.CharField(max_length=50)    

# The Dow Jones Industrial Average Index Composition:
class DJIAIndexComposition(models.Model):
    """
    """
    pass

# S&P/TSX Index Composition:
class SPTSXIndexComposition(models.Model):
    """
    """
    pass

# Financial Times Stock Exchange 100 Index Composition:
class FTSE100IndexComposition(models.Model):
    """
    """
    pass

# Swiss Market Index Composition:
class SMIComposition(models.Model):
    """
    """
    pass

# Swiss Performance Index Composition:
class SPIComposition(models.Model):
    """
    """
    pass