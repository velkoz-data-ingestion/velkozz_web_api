# Importing the Market Index Seralizers, Database Models and Base ModelViewSets:
from accounts.views import AbstractModelViewSet
from finance_api.models.securities_data.securities_ohlc import * 
from .securities_pricing_serializers import * 

# Importing DRF ViewSet packages:
from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import Permission

# Importing Django packages:
from django.core.files import File

# Importing 3rd party packages:
import pandas as pd
import csv
import os
import json
from io import StringIO, BytesIO
import base64

class SecuritiesPriceOHLCViewSet(AbstractModelViewSet):
    """The ViewSets providing the REST API routes for the SecuritiesOHLC Prices
    database table.
    """
    queryset = SecurityPriceOHLC.objects.all()

    def list(self, request, ticker=None):
        """The ViewSet method that processes GET requests made to the
        SecuritiesPriceOHLC API. 

        The method queries the database for data relating to the price
        timeseries .csv files according to the GET url params. Once the
        data has been sucessfully queried it is seralized into a JSON object
        and returned as an HTTP response object.  
        
        Arguments:
            ticker (None | string): A URL param used to specify the security
                being queried. A required parameter.

            TODO: Add Start-Date and End-Date filtering.

        """
        # Extracting the Query Parameters from the request:
        if "ticker" in request.GET:
            ticker = request.GET["ticker"]

        if ticker is None:
            return Response(
                {"Error Message":"Must Provide A Ticker Symbol for OHLC Data"})

        # Extracting URL params used to specify OHLC search:
        start_date = request.GET.get("Start-Date", None)
        end_date = request.GET.get("End-Date", None)

        # Querying the database for the ohlc price via ticker:
        ohlc_security = SecurityPriceOHLC.objects.get(security_ticker=ticker)

        # Converting the price history timeseries to pandas dataframe:
        ohlc_df = pd.read_csv(ohlc_security.price_ohlc, index_col="Date") 

        # Filtering the ohlc_df based on start and end parameters:
        ohlc_df_filtered = ohlc_df[start_date:end_date] 

        # Dataframe to JSON response:
        ohlc_json = ohlc_df_filtered.to_json(orient="index")
        
        # Creating JSON to return via post:
        response_payload = {
            "Ticker": ticker,
            "OHLC_TimeSeries": ohlc_json
            }

        # Formatting to JSON:
        json_payload = json.dumps(response_payload)
        loaded_payload = json.loads(json_payload)
        
        return Response(loaded_payload)
        

    def create(self, request):
        """Method manually performs the data ingestion for security 
        ohlc timeseries for the SecuritiesPriceOHLC API. 

        The method recives JSON data of a price history timeseries csv file encoded in base64. It 
        converts this base64 string into a csv file, which is then read to the database and stored
        via the custom File System Storag class.


        TODO:
            * Add data validation for "OHLC_TimeSeries" parameter to enusre correct format.
            * Look to migrating ingestion/json seralization to a dedicated ModelViewSeralzier if csv conversion
                can be ported. 
            * Explore other methods of storing and retrieving timeseries data. Measure read/write speeds and see
                if dedicated db like InflixDB or TimeScale is a better storage method. 

        Notes: 
            This method does not perform data validation, it assumes data validation. It should be replaced by
            a DRF seralizer.
            
        """
        # Decoding the request body into params:
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        
        ticker = body.get("ticker", None)
        encoded_ohlc = body.get("ohlc", None)

        if ticker is None:
            return Response({"Response":"No POST data found in request.body"})

        # Decoding the Base64 string:
        decoded_ohlc = base64.b64decode(encoded_ohlc)

        # Converting the decoded string to a pandas dataframe:
        ohlc_in_memory = StringIO(decoded_ohlc.decode('utf-8'))
        ohlc_df = pd.read_csv(ohlc_in_memory, sep=",", index_col="Date")

        # Formatting the csv dataframe:
        ohlc_df = ohlc_df.round(2)

        # Converting the dataframe for temporary csv file:
        temp_path = f"{ticker}_ohlc.csv"
        ohlc_df.to_csv(temp_path, index=True, index_label="Date")

        # Creating/Inserting an instance of SecurityPriceOHLC:
        with open(temp_path, "rb") as temp_csv:
            price_ohlc = SecurityPriceOHLC.objects.update_or_create(
                security_ticker = ticker,
                defaults = {'price_ohlc': File(temp_csv)}
                )
                
        # Destroying the temporary csv:
        os.remove(temp_path)

        return Response({
            "Ticker": ticker,
            "OHLC": decoded_ohlc})
