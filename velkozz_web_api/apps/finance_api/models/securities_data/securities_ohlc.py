# Importing native django packages:
from django.db import models
from django.core.exceptions import ObjectDoesNotExist

# Importing custom storage soloution for storing price csv data:
from finance_api.model_views_seralizers.securities_pricing.securities_pricing_storage import OHLCOverwriteStorage

class SecurityPriceOHLC(models.Model):
    """
    TODO: Add Documentation.   
    """
    security_ticker = models.CharField(
        max_length=50,
        primary_key=True,
        unique=True)

    price_ohlc = models.FileField(
        upload_to="finance_api/ohlc",
        unique=True,
        null=True,
        storage=OHLCOverwriteStorage())

    updated_on = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return f"OHLC Price For {self.security_ticker}"

    class Meta:
        verbose_name_plural = "Security OHLC Price Data"