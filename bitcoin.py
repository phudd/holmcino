from django.conf import settings
from jsonrpc.proxy import ServiceProxy

class Bitcoin(object):
    
    def __init__(self, url, method=None):
        self._url = url
        self._proxy = None
        self._method = method
        
    def __getattr__(self, name):
        return Bitcoin(self._url, name)
        
    def __call__(self, *args):
        if (self._proxy == None):
            self._proxy = ServiceProxy(settings.BITCOIN_URL)
        response = self._proxy.__getattr__(self._method)(*args)
        return self.parseResponse(response)
            
    def parseResponse(self, response):
        if response.get(u'error') != None:
            code = response[u'error'].get(u'code', 'no-code')
            code = str(code)
            message = response[u'error'].get(u'message', 'no-message')
            
            raise Exception( code + ': ' + message)
        else:
            return response.get(u'result')
    
