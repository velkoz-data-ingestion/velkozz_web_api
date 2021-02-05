# Importing Django Models:
from django.contrib import admin

# Importing Database Models:
from .stock_api_mvc.market_indicies_models import *

# Registering the Market Indicies Composition Models to the Admin Dashboard:
admin.site.register(SPYIndexComposition)
admin.site.register(DJIAIndexComposition)
admin.site.register(SPTSXIndexComposition)
admin.site.register(FTSE100IndexComposition)
admin.site.register(SMIComposition)
admin.site.register(SPIComposition)
