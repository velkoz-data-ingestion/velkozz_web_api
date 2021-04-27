# Importing Django Models:
from django.contrib import admin

# Importing Database Models:
from .models.market_indicies.market_indicies_models import *
from .models.securities_data.securities_ohlc import *
from .models.structured_quant_data.wsb_data import *

# Registering the Market Indicies Composition Models to the Admin Dashboard:
admin.site.register(SPYIndexComposition)
admin.site.register(DJIAIndexComposition)
admin.site.register(SPTSXIndexComposition)
admin.site.register(FTSE100IndexComposition)
admin.site.register(SMIComposition)
admin.site.register(SPIComposition)
admin.site.register(NYSEComposition)
admin.site.register(NASDAQComposition)

# Registring the Security OHLC Models to the Admin Dashboard:
admin.site.register(SecurityPriceOHLC)

# Registering the Structured Quant Data Models to the Admin Dash:
admin.site.register(WallStreetBetsTickerMentions)