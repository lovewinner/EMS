#!/usr/bin/python
#coding=utf8
import logging
import logging.config
import sys
from pprint import pprint
reload(sys)
sys.setdefaultencoding('utf-8')
import views
from settings import settings, LOGGING
import tornado.httpserver
import tornado.web
from tornado_lib.routes import route
from tornado_lib.run_server import run_server, parse_options


options = parse_options()

urls = route.get_routes()
application = tornado.web.Application(urls, **settings)

pprint(route.get_routes())
run_server(application)
