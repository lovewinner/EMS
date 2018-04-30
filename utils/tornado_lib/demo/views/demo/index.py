#!/user/bin/python
#coding=utf8
from tornado_lib.base import BaseHandler 
from tornado_lib.routes import route

class Index(BaseHandler):
    def get(self):
        self.set_log_var(demo_log='demo')
        self.write('Hello Demo')

    def post(self):
        raise NotImplementedError

@route('/demo/default/(.*)')
class Default(BaseHandler):
    def get(self, arg):
        self.write(arg)

    def post(self):
        raise NotImplementedError

