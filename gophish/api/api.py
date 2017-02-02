import requests
import urllib
import json

from gophish.models import Error

'''
api.py 

Base API endpoint class that abstracts basic CRUD operations.
'''

class APIEndpoint_requests(object):
    """
    Represents an API endpoint for Gophish, containing common patterns
    for CRUD operations.
    """
    def __init__(self, api, endpoint=None, cls=None):
        """ Creates an instance of the APIEndpoint class.

        Args:
            api - Gophish.client - The authenticated REST client
            endpoint - str - The URL path to the resource endpoint
            cls - gophish.models.Model - The Class to use when parsing results
        """
        self.api = api
        self.endpoint = endpoint
        self._cls = cls

    def get(self, resource_id=None):
        """ Gets the details for one or more resources by ID
        
        Args:
            cls - gophish.models.Model - The resource class
            resource_id - str - The endpoint (URL path) for the resource

        Returns:
            One or more instances of cls parsed from the returned JSON
        """

        endpoint = self.endpoint

        if resource_id:
            endpoint = '{}/{}'.format(endpoint, resource_id)

        response = self.api.execute("GET", endpoint)
        if not response.ok:
            return Error.parse(response.json())

        if resource_id:
            return self._cls.parse(response.json())

        return [self._cls.parse(resource) for resource in response.json()]

    def post(self, resource):
        """ Creates a new instance of the resource.

        Args:
            resource - gophish.models.Model - The resource instance

        """
        response = self.api.execute("POST", self.endpoint, json=(resource.as_dict()))
        
        if not response.ok:
            return Error.parse(response.json())

        return self._cls.parse(response.json())

    def put(self, resource):
        """ Edits an existing resource

        Args:
            resource - gophish.models.Model - The resource instance
        """
        
        endpoint = self.endpoint

        if resource.id:
            endpoint = '{}/{}'.format(endpoint, resource.id)

        response = self.api.execute("PUT", endpoint, json=resource.as_json())

        if not respose.ok:
            return Error.parse(response.json())

        return self._cls.parse(response.json())

    def delete(self, resource_id):
        """ Deletes an existing resource

        Args:
            resource_id - int - The resource ID to be deleted
        """

        endpoint = '{}/{}'.format(self.endpoint, resource_id)

        response = self.api.execute("DELETE", endpoint)

        if not response.ok:
            return Error.parse(response.json())

        return self._cls.parse(response.json())

'''
Overwrite of the class from api.py to support urllib instead of Requests

Base API endpoint class that abstracts basic CRUD operations.
'''

class APIEndpoint_urllib(object):
    """
    Represents an API endpoint for Gophish, containing common patterns
    for CRUD operations.
    """
    def __init__(self, api, endpoint=None, cls=None):
        """ Creates an instance of the APIEndpoint class.

        Args:
            api - Gophish.client - The authenticated REST client
            endpoint - str - The URL path to the resource endpoint
            cls - gophish.models.Model - The Class to use when parsing results
        """
        self.api = api
        self.endpoint = endpoint
        self._cls = cls

    def get(self, resource_id=None):
        """ Gets the details for one or more resources by ID
        
        Args:
            cls - gophish.models.Model - The resource class
            resource_id - str - The endpoint (URL path) for the resource

        Returns:
            One or more instances of cls parsed from the returned JSON
        """

        endpoint = self.endpoint

        if resource_id:
            endpoint = '{}{}'.format(endpoint, resource_id)

        try:
            response = self.api.execute("GET", endpoint)
            jresponse = json.loads(response.read().decode('UTF-8'))

            if resource_id:
                return self._cls.parse(jresponse)
    
            return [self._cls.parse(resource) for resource in jresponse]

        except urllib.error.HTTPError as e:
            return Error.parse(jresponse)

    def post(self, resource):
        """ Creates a new instance of the resource.

        Args:
            resource - gophish.models.Model - The resource instance

        """

        endpoint = self.endpoint
        
        try:
            post_data = json.dumps(resource.as_dict()).encode('UTF-8').decode('ascii').encode('UTF-8')
            headers = {'Content-Type': 'application/json'}
            response = self.api.execute("POST", endpoint, data=post_data, headers=headers)
            jresponse = json.loads(response.read().decode('UTF-8'))
            return self._cls.parse(jresponse)

        except urllib.error.HTTPError as e:
            print(e.read())
            if e.code == 400: 
                jresponse = json.loads(e.read().decode('UTF-8'))
                return Error.parse(jresponse)

    def put(self, resource):
        """ Edits an existing resource

        Args:
            resource - gophish.models.Model - The resource instance
        """
        
        endpoint = self.endpoint

        if resource.id:
            endpoint = '{}{}'.format(endpoint, resource.id)

        response = self.api.execute("PUT", endpoint, json=resource.as_json())

        if not respose.ok:
            return Error.parse(response.json())

        return self._cls.parse(response.json())

    def delete(self, resource_id):
        """ Deletes an existing resource

        Args:
            resource_id - int - The resource ID to be deleted
        """

        endpoint = self.endpoint

        endpoint = '{}{}'.format(endpoint, resource_id)

        try:
            headers = {'Content-Type': 'application/json'}
            response = self.api.execute("DELETE", endpoint)
            jresponse = json.loads(response.read().decode('UTF-8'))
            return self._cls.parse(jresponse)

        except urllib.error.HTTPError as e:
            print(e.read())
            if e.code == 400: 
                jresponse = json.loads(e.read().decode('UTF-8'))
                return Error.parse(jresponse)


APIEndpoint = APIEndpoint_urllib
#APIEndpoint = APIEndpoint_requests
