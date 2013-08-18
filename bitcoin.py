from django.conf import settings
from jsonrpc.proxy import ServiceProxy

class Bitcoin(object):
    
    def __init__(self, url):
        self.proxy = ServiceProxy(settings.BITCOIN_URL)

    def validateaddress(self, address):
        result = self.proxy.validateaddress(address)
        return self.parseResult(result)
    
    def parseResult(self, result):
        if result.get(u'error') != None:
            raise Exception( str(result.error.get(u'code', 'no-code')) + ': ' + result.error.get(u'message') )
        else:
            return result.get('result')
    
