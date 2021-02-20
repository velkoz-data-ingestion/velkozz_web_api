# Importing Data management packages: 
import json
from collections import OrderedDict
from datetime import datetime

# Importing Testing Framework:
from rest_framework import status
from django.test import TestCase, Client
from django.urls import reverse
from rest_framework.test import APIRequestFactory, force_authenticate
from rest_framework.request import Request
from django.forms.models import model_to_dict
from django.contrib.auth.models import Group

# Importing Account Data Models; 
from accounts.models import CustomUser

# Declaring global config objects that the Abstract TestCase Uses:
factory = APIRequestFactory()

class AbstractRedditModelTestCase():
    """An Abstract Method that is extended by a TestCase class for testing a
    Reddit data REST API.

    This object is meant to contain the boilerplate logic and testing methods
    to implement testing of the REST API for Reddit Data Models and ViewSets.

    In order for this model to be extended sucessfully it requires the Child
    method to provide a setUp class that contains the following instance fields:

    self.RedditModel - The Reddit Database Model to be tested.  
    self.ModelViewSet - The Model Viewset to be tested
    self.api_url - The endpoint of the REST API.

    All test data should be written to the database in the setUp() method aswell
    via a bulk_create command or use of the self.RedditModel.create() methods.

    """
    def setUp(self):
        """Creating custom user with necesary permissions for use in testing:
        """
        # Extracting the group objects for API users:
        free_tier = Group.objects.create(name="api_free_tier")
        free_tier.save()

        # Assign Permissions to the Group itself.

        #api_professional_tier = Group.objects.get(name="api_professional_tier")

        # Creating users with differing permissions:
        self.test_user_free = CustomUser.objects.create_user(
            "test_user_free", "testuser@example.com", "password123")
        self.test_user_professional = CustomUser.objects.create_user(
            "test_user_pro", "protestuser@example.com", "password123")
        
        self.test_user_free.save()
        self.test_user_professional.save()

        # Assigning permission groups to users:
        free_tier.user_set.add(self.test_user_free)
        #api_professional_tier.user_set.add(test_user_professional)

        

    def test_GET_request(self):
        """A boilerplace method that tests the standard GET requet functionality
        of the database.
        
        If additonaly functionality needs to be added to this method such as 
        testing for query parameters the method can be extended by the Child
        TestCase. 

        The method by default performs a GET request to the specific endpoint,
        makes a backend database query through the data model and compares
        these two objects to ensure that the two are equal. 

        This ensures that the GET request is sucessfully reading data from
        the database. 

        """        
        # Performing a GET Request to the endpoint:
        get_request = factory.get(self.api_url, format='json')
        force_authenticate(user=self.test_user_free, request=get_request)

        # Querying the database for all model instances:
        database_response = self.RedditModel.objects.all()
        database_json_response = list(database_response.values())

        # Extract keys that are returned from the JSON to filter the GET requeust:
        db_model_keys = database_json_response[0].keys()

        # Extracting content from the API GET request:
        view = self.ModelViewSet.as_view({'get': 'list'})
        get_response = view(get_request)

        # Iterating through the list of QueryDicts filtering for only the keys extracted
        # from the database model query:
        get_request = get_response.data 
        filtered_get_request = [
            OrderedDict([(key, qset[key]) for key in qset.keys() if key in set(db_model_keys)]) 
            for qset in get_request
        ]

        # Converting the get_request QueryDict to json:
        get_request_json = json.loads(json.dumps(filtered_get_request))
        # Converting the datetime strings from the GET request to a datetime object:
        for item in get_request_json:
            
            item['author_created'] = datetime.strptime(
                item["author_created"], "%Y-%m-%dT%H:%M:%S%z")

            item["created_on"] = datetime.strptime(
                item["created_on"], "%Y-%m-%dT%H:%M:%S%z")
            
        # Performing Assertion Testing: 
        print(f"\nPerforming GET Request Testing for Reddit API {self.ModelViewSet} on Database Model {self.RedditModel}")

        # Ensuring a 200 status code:
        self.assertEqual(get_response.status_code, 200)

        # Comparing the GET request data to the data extracted from the database model:
        self.assertEqual(database_json_response, get_request_json)
    
    def test_POST_requests(self):
        """The method tests the ability of the REST API to sucessfully
        ingest data.

        If additonaly functionality needs to be added to this method such as 
        testing for query parameters the method can be extended by the Child
        TestCase. 

        The method performs a POST request to the database, writing data. A 
        GET request is then made which is compared to a backend database query
        to ensure that the additional data has been added correctly to the database.

        """
        # Declaring data in a json fromat:
        data_payload = [
            {
                "id": "poiumn",
                "title": "A Test for the POST",
                "content" : "This is some Test Content",
                "upvote_ratio" : 0.77,
                "score" : 2625,
                "num_comments" : 580,
                "created_on" : "2021-02-09T02:08:58Z",
                "stickied" : False,
                "over_18" : False,
                "spoiler" : False,
                "author_gold" : False,
                "mod_status" : False,
                "verified_email_status" : True,
                "permalink" : "/r/wallstreetbets/comments/lfs22f/why_ill_never_stop_buying_gme_and_why_you/",
                "author" : "A_test_author",
                "acc_created_on" : "2019-08-20T02:31:19Z",
                "comment_karma" : 2504
            },
                        {
                "id": "cvbf53",
                "title": "A Test for the POST",
                "content" : "This is some Test Content",
                "upvote_ratio" : 0.77,
                "score" : 2625,
                "num_comments" : 580,
                "created_on" : "2021-02-09T02:08:58Z",
                "stickied" : False,
                "over_18" : False,
                "spoiler" : False,
                "author_gold" : False,
                "mod_status" : False,
                "verified_email_status" : True,
                "permalink" : "/r/wallstreetbets/comments/lfs22f/why_ill_never_stop_buying_gme_and_why_you/",
                "author" : "A_test_author",
                "acc_created_on" : "2019-08-20T02:31:19Z",
                "comment_karma" : 2504
            }
        ]

        # Performing a POST request to the database via APIFactory:
        post_request = factory.post(self.api_url, data_payload, format="json")
        force_authenticate(user=self.test_user_free, request=post_request)
    
        # Extracting content from the API GET request:
        view = self.ModelViewSet.as_view({'post': 'create'})
        get_response = view(post_request)

        # Querying the database for all model instances:
        database_response = self.RedditModel.objects.all()
        database_json_response = list(database_response.values())

        # Extract keys that are returned from the JSON to filter the GET requeust:
        db_model_keys = database_json_response[0].keys()
        
        # Iterating through the list of QueryDicts filtering for only the keys extracted
        # from the database model query:
        get_request = get_response.data 

        filtered_get_request = [
            OrderedDict([(key, qset[key]) for key in qset.keys() if key in set(db_model_keys)]) 
            for qset in get_request
        ]

        # Converting the get_request QueryDict to json:
        get_request_json = json.loads(json.dumps(filtered_get_request))
        # Converting the datetime strings from the GET request to a datetime object:
        for item in get_request_json:
            
            item['author_created'] = datetime.strptime(
                item["author_created"], "%Y-%m-%dT%H:%M:%S%z")

            item["created_on"] = datetime.strptime(
                item["created_on"], "%Y-%m-%dT%H:%M:%S%z")
            
        # Performing Assertion Testing: 
        print(f"\nPerforming POST Request Testing for Reddit API {self.ModelViewSet} on Database Model {self.RedditModel}")

        # Ensuring a 200 status code:
        self.assertEqual(get_response.status_code, 200)

        # Comparing the GET request data to the data extracted from the database model:
        self.assertEqual(database_json_response, get_request_json)
