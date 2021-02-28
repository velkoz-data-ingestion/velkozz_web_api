# Importing Django Models:
from django.contrib import admin

# Importing Database Models:
from .models.market_indicies.market_indicies_models import *
from .models.securities_data.securities_ohlc import *

# Registering the Market Indicies Composition Models to the Admin Dashboard:
admin.site.register(SPYIndexComposition)
admin.site.register(DJIAIndexComposition)
admin.site.register(SPTSXIndexComposition)
admin.site.register(FTSE100IndexComposition)
admin.site.register(SMIComposition)
admin.site.register(SPIComposition)

# Registring the Security OHLC Models to the Admin Dashboard:
admin.site.register(SecurityPriceOHLC)