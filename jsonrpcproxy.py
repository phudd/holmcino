import urllib
import uuid
import json
from django.conf import settings

class ClientProxy(object):
    """ This is a proxy object for a json-rpc service.  I initially borrowed from 
        django-json-rpc, but eventually departed to create my own proxy.
    
        Once initialized, you can call any function freely.  Errors raise exceptions.  Other
        kinds of responses are returned unmolested.  The overhead fields are thrown away.
    """
    def __init__(self, url):
        self._url = url
        
    def __getattr__(self, name):
        """ Attributes are all functions.  Build a function with the right closure, so it
            can be called with the desired parameters.
        """
        def callfunc(*args, **kwargs):
            jsoncall = {
                'jsonrpc':"2.0",
                'id': str(uuid.uuid1()),
                'method': name,
                'params': kwargs if len(kwargs) else args
            }
            response = urllib.urlopen(self._url, json.dumps(jsoncall)).read()
            response = json.loads(response)
            return self.parseResponse(response)

        return callfunc
                    
    def parseResponse(self, response):
        if response.get(u'error') != None:
            code = response[u'error'].get(u'code', 'no-code')
            code = str(code)
            message = response[u'error'].get(u'message', 'no-message')
            
            raise Exception( code + ': ' + message)
        else:
            return response.get(u'result')
    
