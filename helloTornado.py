import os
import time
import json
import tornado.httpserver
import tornado.web
import tornado.ioloop
import tornado.wsgi
import sys
import django.core.handlers.wsgi
from tornado import websocket
from crapsTable import CrapsPlayer

#sys.path.append('/home/lawgon/') # path to your project ( if you have it in another dir).

def main():
    # os.environ['DJANGO_SETTINGS_MODULE'] = 'project.settings' # path to your settings module
    # application = django.core.handlers.wsgi.WSGIHandler()
    # container = tornado.wsgi.WSGIContainer(application)
    manyApp = tornado.web.Application([
        (r'^/craps/([^\/]+)$', CrapsPlayer),
        # (r'.*', container),
    ])
    http_server = tornado.httpserver.HTTPServer(manyApp)
    http_server.listen(8888)
    tornado.ioloop.IOLoop.instance().start()

if __name__ == "__main__":
    main()
