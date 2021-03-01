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
from io import StringIO

class SecuritiesPriceOHLCViewSet(AbstractModelViewSet):
    """
    TODO: Add Documentation.
    """
    queryset = SecurityPriceOHLC.objects.all()

    def list(self, request, ticker=None):
        """
        TODO: Add Documentation
        """
        # Extracting the Query Parameters from the request:
        if "ticker" in request.GET:
            ticker = request.GET["Ticker"]

        if ticker is None:
            return Response("Must Provide A Ticker Symbol for OHLC Data")

        # Querying the database for the ohlc price via ticker:
        ohlc_security = SecurityPriceOHLC.objects.get(security_ticker=ticker)

        # Converting the price history timeseries to pandas dataframe:
        ohlc_df = pd.read_csv(ohlc_security.price_ohlc, index_col="DateTime") 

        # Dataframe to JSON response:
        ohlc_json = ohlc_df.to_json(orient="index")
        
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
        ohlc timeseries. 

        The method takes pre-formatted data from a POST request  in the format:
        [
            {
            "Ticker": "XXXX",
            "OHLC_TimeSeries": {
                date1: {"Open": x, "High": x, "Low": x, "Close": x. "Dividends": x, "Stock Splits": x},
                date2: {"Open": x, "High": x, "Low": x, "Close": x. "Dividends": x, "Stock Splits": x},
                date3: {"Open": x, "High": x, "Low": x, "Close": x. "Dividends": x, "Stock Splits": x}
                }
            },
            {
            "Ticker": "YYYY",
            "OHLC_TimeSeries": {
                date1: {"Open": x, "High": x, "Low": x, "Close": x. "Dividends": x, "Stock Splits": x},
                date2: {"Open": x, "High": x, "Low": x, "Close": x. "Dividends": x, "Stock Splits": x},
                date3: {"Open": x, "High": x, "Low": x, "Close": x. "Dividends": x, "Stock Splits": x}
                }
            }
        ]

        It converts this JSON data into a pandas dataframe which is formatted correctly and then converted
        into a csv file which is ingested into the appropriate Django FileField. 

        Notes: 
            This method does not perform data validation, it assumes data validation. It should be replaced by
            a DRF seralizer.
            
        """
        # Extracting POST request data:
        if request.body:
            post_data = json.loads(request.body)
        
        else:
            return Response({"Response":"No POST data found in request.body"})


        # Parsing the POST data and creating a .csv file:
        for security in post_data:
            
            ohlc_df = pd.DataFrame.from_dict(
                security["OHLC_TimeSeries"], orient="index")

            # Formatting the csv dataframe:
            ohlc_df = ohlc_df.round(2)

            # Converting the dataframe for temporary csv file:
            temp_path = f"{security['Ticker']}_ohlc.csv"
            ohlc_df.to_csv(temp_path, index=True, index_label="DateTime")

            # Creating/Inserting an instance of SecurityPriceOHLC:
            with open(temp_path, "rb") as temp_csv:
        
                price_ohlc = SecurityPriceOHLC.objects.update_or_create(
                    security_ticker = security["Ticker"],
                    defaults = {'price_ohlc': File(temp_csv)},
                )
                
            # Destroying the temporary csv:
            os.remove(temp_path)

        return Response(post_data)
