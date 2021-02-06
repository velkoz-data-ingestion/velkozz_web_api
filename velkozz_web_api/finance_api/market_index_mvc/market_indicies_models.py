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
    date_added = models.CharField(max_length=25, null=True)
    cik = models.IntegerField(unique=True)
    founded = models.CharField(max_length=50)    

    def __str__(self):
        return self.symbol

    class Meta:
        verbose_name_plural = "SPY Market Index Composition"

# The Dow Jones Industrial Average Index Composition:
class DJIAIndexComposition(models.Model):
    """A data model representing a database table containing information
    on the Dow Jones Industrial Average Index. 

    It is built for the velkozz API with the ETL pipeline API in mind for POST
    requsts. There is no primary key declared, the model makes use of django's 
    automatic primary key pk. 

    Attributes:

        company (models.CharField): The company name.

        exchange (models.CharField): The exchange that the stock is a part of.

        symbol (models.CharField): The ticker symbol of the company. 

        industry (models.CharField): The industry category that the company is a part of.
        
        date_added (models.DateField): The date that the company was added to the DJIA.
        
        notes (models.CharField): Any additional notes for the company.

        weighting (models.CharField): What percentage of the index is made up of the company.

    """
    company = models.CharField(max_length=150, unique=True)
    exchange = models.CharField(max_length=15)
    symbol = models.CharField(max_length=10, unique=True)
    industry = models.CharField(max_length=150)
    date_added = models.DateTimeField()
    notes = models.CharField(max_length=200, null=True)
    weighting = models.CharField(max_length=20, null=True)

    def __str__(self):
        return self.symbol

    class Meta:
        verbose_name_plural = "DJIA Market Index Composition"

# S&P/TSX Index Composition:
class SPTSXIndexComposition(models.Model):
    """A data model representing a database table containing information
    on the S&P/TSX Composite Index. 

    It is built for the velkozz API with the ETL pipeline API in mind for POST
    requsts. There is no primary key declared, the model makes use of django's 
    automatic primary key pk. 

    Attributes:

        symbol (models.CharField): The ticker symbol of the company. 

        company (models.CharField): The company name.

        sector (models.CharField): The sector category that the company is a part of.
        
        industry (models.CharField): The industry category that the company is a part of.

    """
    symbol = models.CharField(max_length=20, unique=True)
    company = models.CharField(max_length=200)
    sector = models.CharField(max_length=100)
    industry = models.CharField(max_length=200)

    def __str__(self):
        return self.symbol

    class Meta:
        verbose_name_plural = "S&P/TSX Market Index Composition"


# Financial Times Stock Exchange 100 Index Composition:
class FTSE100IndexComposition(models.Model):
    """A data model representing a database table containing information
    on the Financial Times Stock Exchange 100 Index. 

    It is built for the velkozz API with the ETL pipeline API in mind for POST
    requsts. There is no primary key declared, the model makes use of django's 
    automatic primary key pk. 

    Attributes:

        company (models.CharField): The company name.

        symbol (models.CharField): The ticker symbol of the company. 
        
        industry (models.CharField): The industry category that the company is a part of.

    """
    company = models.CharField(max_length=150, unique=True)
    symbol = models.CharField(max_length=10, unique=True)
    industry = models.CharField(max_length=200)

    def __str__(self):
        return self.symbol

    class Meta:
        verbose_name_plural = "FTSE 100 Market Index Composition"

# Swiss Market Index Composition:
class SMIComposition(models.Model):
    """A data model representing a database table containing information
    on the Swiss Market Index. 

    It is built for the velkozz API with the ETL pipeline API in mind for POST
    requsts. There is no primary key declared, the model makes use of django's 
    automatic primary key pk. 

    Attributes:

        rank (models.CharField): The rank of the company in the index.
        
        company (models.CharField): The company name.

        industry (models.CharField): The industry category that the company is a part of.

        symbol (models.CharField): The ticker symbol of the company. 

        canton (models.CharField): The canton that the company is located.

        weighting (models.CharField): What percentage of the index is made up of the company.

    """
    rank = models.IntegerField()
    company = models.CharField(max_length=100, unique=True)
    industry = models.CharField(max_length=100)
    symbol = models.CharField(max_length=10, unique=True)
    canton = models.CharField(max_length=100)
    weighting = models.CharField(max_length=20)

    def __str__(self):
        return self.symbol

    class Meta:
        verbose_name_plural = "Swiss Market Index Composition"

# Swiss Performance Index Composition:
class SPIComposition(models.Model):
    """A data model representing a database table containing information
    on the Swiss Performance Index. 

    It is built for the velkozz API with the ETL pipeline API in mind for POST
    requsts. There is no primary key declared, the model makes use of django's 
    automatic primary key pk. 

    Attributes:

        symbol (models.CharField): The ticker symbol of the company. 
        
        company (models.CharField): The company name.

        smi_family (models.CharField): The swiss market index that the company is part of.

        date_added (models.CharField): The year that the company was added to the index.

        notes (models.CharField): Any additional notes assocaited to the company. 

    """
    symbol = models.CharField(max_length=10, unique=True)
    company = models.CharField(max_length=100)
    smi_family = models.CharField(max_length=100, null=True)
    date_added = models.CharField(max_length=10, null=True)
    notes = models.CharField(max_length=200, null=True)

    def __str__(self):
        return self.symbol

    class Meta:
        verbose_name_plural = "Swiss Performance Index Composition"
