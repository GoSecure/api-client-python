import requests
from urllib.request import build_opener, install_opener, HTTPSHandler, \
                                    Request, urlopen


from gophish.api import (
    campaigns,
    groups,
    pages,
    smtp,
    templates)

DEFAULT_URL = 'http://localhost:3333'

class GophishClient(object):
    """ A standard HTTP REST client used by Gophish """
    def __init__(self, api_key, host=DEFAULT_URL, **kwargs):
        self.api_key = api_key
        self.host = host
        self._client_kwargs = kwargs
    
    def _execute_requests(self, method, path, kwargs):
        """ Executes a request using the requests HTTP library """

        url = "{}{}".format(self.host, path)
        kwargs.update(self._client_kwargs)
        response = requests.request(method, url, params={"api_key": self.api_key}, **kwargs)
        return response

    def _execute_urllib(self, method, path, kwargs):
        """ Executes a request using the urllib HTTP library """

        url = "{}{}?api_key={}".format(self.host, path, self.api_key)
        kwargs.update(self._client_kwargs)
        req = Request(url,**kwargs)
        req.get_method = lambda: method
        response = urlopen(req)
        return response

    def execute(self, method, path, **kwargs):
        """ Executes a request to a given endpoint, returning the result 
		Temporary mapping between 2 sub-functions for tests """

        #return self._execute_requests(method, path, kwargs)
        return self._execute_urllib(method, path, kwargs)

class Gophish(object):
    def __init__(self, api_key, host=DEFAULT_URL, client=GophishClient, **kwargs):
        self.client = client(api_key, host=host, **kwargs)
        self.campaigns = campaigns.API(self.client)
        self.groups = groups.API(self.client)
        self.pages = pages.API(self.client)
        self.smtp = smtp.API(self.client)
        self.templates = templates.API(self.client)
