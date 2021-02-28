# Importing Base TestCase containing user validation: 
from accounts.tests.base_testcases import BaseAPITestCase

# Importing Django Testing Framework:
from django.test import TestCase
from django.contrib.auth.models import Group, Permission

# DRF Testing methods:
from rest_framework.test import APIRequestFactory, force_authenticate
from rest_framework.request import Request

# Importing local MVC elements for testing:
from finance_api.models.securities_data.securities_ohlc import SecurityPriceOHLC
from finance_api.model_views_seralizers.securities_pricing.securities_pricing_serializers import SecuritiesPriceOHLCSerializer 
from finance_api.model_views_seralizers.securities_pricing.securities_pricing_views import SecuritiesPriceOHLCViewSet

# Importing external packages:
import pandas as pd
import yfinance as yf
import json

class SecurityOHLCAPITestCase(BaseAPITestCase):
    """TestCase for the Security OHLC API. It contains tests that
    perform CRUD operations for the Security OHLC API endpoint. 
    

    These test methods are necessary as this API stores timeseries data
    using a unique combination of database models and static files. The 
    assertion tests ensure that said timeseries data can be accuratley
    written and read from the server.
    
    """
    def setUp(self):

        # Initalizing Base TestCase Setup:
        super().setUp()

        # API TestClient:
        self.api_client = APIRequestFactory()

        # Extracting test OHLC timeseries to test ingestion:
        self.aapl_ohlc = yf.Ticker("AAPL").history(period="max")
        self.msft_ohlc = yf.Ticker("MSFT").history(period="max")
        self.xom_ohlc = yf.Ticker("XOM").history(period="max")

        # Converting the pandas dataframe to JSON format:
        self.aapl_result = self.aapl_ohlc.to_json(orient="index")
        self.json_parsed_aapl = json.loads(self.aapl_result)
        
        self.msft_result = self.msft_ohlc.to_json(orient="index")
        self.json_parsed_msft = json.loads(self.msft_result)

        # Defining the custom API endpoint:
        self.ohlc_endpoint = "/finance_api/securities/ohlc_timeseries/"

        # Adding OHLC Price data permissions to the ingestion user:
        ohlc_permissions = Permission.objects.all().filter(
            codename__contains="securitypriceohlc")

        for permission in ohlc_permissions:
            self.ingestion_acc.user_permissions.add(permission)

    def test_ohlc_POST_request(self):
        """Method takes the extracted ohlc dataframes declared in
        startUp and makes a POST request to the database through the
        API endpoint.

        The method tests that the ingestion was sucessfull
        as well as the accuracy of the ingestion.
        """
        # Performing Inital Query for empty database:
        empty_queryset = SecurityPriceOHLC.objects.all()

        self.assertEqual(len(empty_queryset), 0)

        # Creating data payload:
        data_payload = [
            {
                "Ticker" : "AAPL",
                "OHLC_TimeSeries" : self.json_parsed_aapl
            }
        ]

        # Performing POST request to the viewset:
        post_request = self.api_client.post(self.ohlc_endpoint, data_payload, format="json")
        force_authenticate(user=self.ingestion_acc, request=post_request)   

        view = SecuritiesPriceOHLCViewSet.as_view({"post":"create"})
        post_response = view(post_request)

        # Asserting that the POST request was validated:
        self.assertEqual(post_response.status_code, 200)

        # Querying the database for newly created data:
        ohlc_queryset = SecurityPriceOHLC.objects.all()

        # Ensuring data has been written to the database:
        self.assertEqual(len(ohlc_queryset), 1)

        # Ensuring Correct data was written to db:
        self.assertEqual(ohlc_queryset[0].security_ticker, data_payload[0]["Ticker"])
        self.assertEqual(
            ("csv" in ohlc_queryset[0].price_ohlc.name), True)

        print("\nPerformed POST Request test to Finance API <SecuritiesPriceOHLCViewSet> w/ OHLC data.")

    def test_ohlc_GET_request(self):
        """Method performs a GET request for the aapl and msft ohlc data 
        stored in the database and tests if the ViewSet and Seralizer 
        returns price timeseries data in the correct json format.

        """
        # Performing a POST request to populate the database:

        # Performing Inital Query for empty database:
        empty_queryset = SecurityPriceOHLC.objects.all()

        self.assertEqual(len(empty_queryset), 0)

        # Creating data payload:
        data_payload = [
            {
                "Ticker" : "AAPL",
                "OHLC_TimeSeries" : self.json_parsed_aapl
            }
        ]

        # Performing POST request to the viewset:
        post_request = self.api_client.post(self.ohlc_endpoint, data_payload, format="json")
        force_authenticate(user=self.ingestion_acc, request=post_request)   

        view = SecuritiesPriceOHLCViewSet.as_view({"post":"create"})
        post_response = view(post_request)
        
        # Asserting that the POST request was validated:
        self.assertEqual(post_response.status_code, 200)

        # Performing GET request to the API for AAPL price data:
        get_request = self.api_client.get(self.ohlc_endpoint, format="json")
        force_authenticate(user=self.ingestion_acc, request=get_request)

        view = SecuritiesPriceOHLCViewSet.as_view({"get":"list"})
        get_response = view(get_request, ticker="AAPL")

        # Asserting that the GET request was validated:
        self.assertEqual(get_response.status_code, 200)

        print(get_response.data)


