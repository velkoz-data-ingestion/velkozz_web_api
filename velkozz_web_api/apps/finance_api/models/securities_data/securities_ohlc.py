# Importing native django packages:
from django.db import models


class SecurityPriceOHLC(models.Model):
    """
    TODO: Add Documentation.
   
    TODO: Catch the django pre-save signal to only update csv files w/ same name:
        * https://stackoverflow.com/questions/9522759/imagefield-overwrite-image-file-with-same-name
        * https://stackoverflow.com/questions/51075396/python-django-does-not-overwrite-newly-uploaded-file-with-old-one
    """
    security_ticker = models.CharField(
        max_length=50,
        primary_key=True,
        unique=True)

    price_ohlc = models.FileField(
        upload_to="finance_api/ohlc",
        unique=True,
        null=True)

    updated_on = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return f"OHLC Price For {self.security_ticker}"

    class Meta:
        verbose_name_plural = "Security OHLC Price Data"