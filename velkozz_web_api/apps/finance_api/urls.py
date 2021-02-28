# Importing Django Methods:
from django.urls import include, path
from rest_framework import routers

# Importing the Market Index Composition Views from the Market Index MVC:
from .model_views_seralizers.market_index import market_indicies_views

# Importing the Security OHLC Views from the Securities Data MVC:
from .model_views_seralizers.securities_pricing import securities_pricing_views

# Creating Url Router:
router = routers.DefaultRouter()

# Registering the Market Indicies Composition API routes:
router.register(r"market_index/spycomp", market_indicies_views.SPYIndexCompositionViewSet)
router.register(r"market_index/djiacomp", market_indicies_views.DJIAIndexCompositionViewSet)
router.register(r"market_index/sptsxcomp", market_indicies_views.SPTSXIndexCompositionViewSet)
router.register(r"market_index/ftse100comp", market_indicies_views.FTSE100IndexCompositionViewSet)
router.register(r"market_index/smicomp", market_indicies_views.SMICompositionViewSet)
router.register(r"market_index/spicomp", market_indicies_views.SPICompositionViewSet)

# Registering the Securities Data API Routes:
router.register(r"securities/ohlc_timeseries", securities_pricing_views.SecuritiesPriceOHLCViewSet)

# Creating Automatic URL Routing:
urlpatterns = router.urls