#!/usr/bin/env python
# -*- coding: utf-8 -*-
import logging
import logging.config
import sys
import time
from gevent import monkey
monkey.patch_all()
import gevent
from pprint import pprint
reload(sys)
sys.setdefaultencoding('utf-8')
import views
import settings
import tornado.httpserver
import tornado.web
from tornado_lib.routes import route
from tornado_lib.run_server import run_server, parse_options
#from tornado_lib.monkey import GeventApplication as Application
#from tornado.web import Application
from tornado.wsgi import WSGIApplication as Application


urls = route.get_routes()
application = Application(urls, **settings.settings)

app = application
