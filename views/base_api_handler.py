import json
import random
import uuid
from tornado_lib.base import BaseHandler
from tornado_lib.routes import route
from tornado.util import bytes_type, unicode_type


_TO_UNICODE_TYPES = (unicode_type, type(None))


class BaseAPIHandler(BaseHandler):
    
    def __init__(self, *args, **kwargs):
        BaseHandler.__init__(self, *args, **kwargs)

    def render_json(self, data):
        self.set_header('Content-Type', 'application/json')
        data = json.dumps(data)
        self.write(data)

    def success(self, result):
        self.render_json({
            "message" : "success",
            "result" : result
        })

    def failed(self, result):
        self.render_json({
            "message" : "failed",
            "result" : result
        })