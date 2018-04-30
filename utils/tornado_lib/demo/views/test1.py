#!/user/bin/python
#coding=utf8
from tornado_lib.base import BaseHandler 
from tornado_lib.routes import route
import time
import logging
from tornado.ioloop import IOLoop
from tornado import gen
from tornado.web import asynchronous
from tornado_lib.decorators import auth_check

class Index(BaseHandler):
    
    @auth_check
    def get(self):
        print 'aaa'
        self.set_log_var(demo_log='demo')
        logging.info("test begin")

        
    def post(self):
        raise NotImplementedError

class Default(BaseHandler):
    def get(self, arg):
        self.write(arg)

    def post(self):
        raise NotImplementedError

