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