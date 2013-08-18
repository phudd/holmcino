import urllib
import uuid
import json
from django.conf import settings

class ClientProxy(object):
    """ This is a proxy object for remote services that implement JSON-RPC 2.0
    
    Once initialized you can call any method of the service just like you would if it 
    were a member function of the object.  For example:
    
        service = ClientProxy('https://some.dom/service_uri')
        var = service.somefunc(var1, var2)
    
    Responses are returned already decoded, and without any of the RPC overhead data.
    
    Errors raise exceptions.  The numeric code of the message is added as a 'code' attribute
    of the exception.
    
    If you pass one of more named arguments to the service, then only the named arguments 
    are sent to the remote method.  In this case, a single dictionary object is sent as the
    param, instead of an array.
    """
    
    def __init__(self, url):
        """ Initialize the proxy with a URL to the remote service."""
        self._url = url
        
    def __getattr__(self, name):
        """ Returns a closure you can use to call the intended remote method."""
        def callfunc(*args, **kwargs):
            jsoncall = {
                'jsonrpc':"2.0",
                'id': str(uuid.uuid1()),
                'method': name,
                'params': kwargs if len(kwargs) else args
            }
            response = urllib.urlopen(self._url, json.dumps(jsoncall)).read()
            self._lastResponse = response
            return self.parseResponse(response)

        return callfunc
                    
    def parseResponse(self, response):
        response = json.loads(response)
        if response.get(u'error') != None:
            code = response[u'error'].get(u'code', 0)
            code = int(code)
            message = response[u'error'].get(u'message', 'no-message')
            
            ex = Exception(str(code) + ': ' + message)
            ex.code = code
            raise ex
        else:
            return response.get(u'result')
    
