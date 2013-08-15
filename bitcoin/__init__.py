from jsonrpc.proxy import ServiceProxy

class Bitcoin:
    def __call__(self, *args, **kwargs):
        retval = ServiceProxy.__call__(self, *args, **kwargs)
        
        if retval.error is not None:
            if u'message' in retval.error:
                raise Exception(retval.error.message)
            elif u'code' in retval.error:
                raise Exception(retval.error.code)
            else:
                raise Exception(str(retval.error))
        else:
            retval = retval.result
        
        return retval
