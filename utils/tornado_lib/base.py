#!/user/bin/python
#coding=utf8
from gevent import monkey
monkey.patch_all()
import gevent
from tornado.web import RequestHandler, access_log
from routes import UrlHandler
import json
from collections import OrderedDict
import uuid
from tornado.stack_context import StackContext
import contextlib
from tornadorpc.json import JSONRPCHandler as BaseJSONRPCHandler
from session import Session, RedisSessionStore
import sys

import redis
import tornado.web
import tornado.wsgi


class BaseHandler(RequestHandler, UrlHandler):
    session_cookie_name = 'sid'
    def __init__(self, *args, **kwargs):
        RequestHandler.__init__(self, *args, **kwargs)
        UrlHandler.__init__(self)

        self.template_var = {}
        self.log_var = OrderedDict()
        
        self.errno = 0

    """
    def _execute(self, transforms, *args, **kwargs):
        @contextlib.contextmanager
        def transfer_log_id():
            ext.thread_data.request = self.log_id
            try:
                yield
            except Exception:
                logging.error("exception in asynchronous operation", exc_info=True)
                sys.exit(1)
        with StackContext(transfer_log_id):
            return super(BaseHandler, self)._execute(transforms, *args, **kwargs)
    """

    def render_json_string(self, data, content_type='application/json'):
        self.set_header('Content-Type', content_type)
        data = json.dumps(data)
        return data

    def render_json(self, data, content_type='application/json'):
        self.write(self.render_json_string(data))
        self.finish()

    def set_log_var(self, **kwargs):
        self.log_var.update(kwargs)

    def set_template_var(self, **kwargs):
        self.template_var.update(**kwargs)

    def check_etag_header(self):
        return False

    def _request_summary(self):
        extra_log_info = ' '.join(['%s[%s]' % (k, v) for k, v in self.log_var.items()])
        try:
            return 'method[%s] uri[%s] remote_ip[%s] user[%s] %s' % (self.request.method, self.request.uri, self.request.remote_ip, self.current_user, extra_log_info)
        except:
            return 'method[%s] uri[%s] remote_ip[%s] user[none] %s' % (self.request.method, self.request.uri, self.request.remote_ip, extra_log_info)

    @classmethod
    def log_function(self, handler):
        if handler.get_status() < 400:
            log_method = access_log.info
        elif handler.get_status() < 500:
            log_method = access_log.warning
        else:
            log_method = access_log.error
        request_time = 1000.0 * handler.request.request_time()
        slow_request = 0 
        if request_time >= 500 :
            slow_request = 1
        log_method("status[%d] %s runtimes_ms[%.2f] slow_request[%d]", handler.get_status(),
                   handler._request_summary(), request_time, slow_request)


    @property
    def session(self):
        if hasattr(self, '_session'):
            return self._session
        session_store = getattr(self.application, 'session_store', None)
        if session_store:
            sessionid = self.get_secure_cookie(self.session_cookie_name)
            s = Session(session_store, sessionid)
            self.set_secure_cookie(self.session_cookie_name, s.sessionid)
            self._session = s
            return s
        return {}

    def get_template_namespace(self, *args, **kwargs):
        res = RequestHandler.get_template_namespace(self, *args, **kwargs)
        res.update(self.template_var)
        res['settings'] = self.settings
        return res
        
class JSONRPCHandler(BaseJSONRPCHandler):
    def post(self):
        # Very simple -- dispatches request body to the parser
        # and returns the output
        self._results = []
        request_body = self.request.body
        self._RPC_.run(self, request_body)


class SessionApplication(tornado.web.Application):
    def __init__(self, handlers, **kwargs):
        tornado.web.Application.__init__(self, handlers, **kwargs)
        session_store = self.settings.get('session_store', None)
        if session_store:
            self.redis = redis.StrictRedis(**session_store)
            self.session_store = RedisSessionStore(self.redis)
        else:
            self.session_store = None


class WsgiSessionApplication(tornado.wsgi.WSGIApplication):
    def __init__(self, handlers, **kwargs):
        tornado.wsgi.WSGIApplication.__init__(self, handlers, **kwargs)
        session_store = self.settings.get('session_store', None)
        if session_store:
            self.redis = redis.StrictRedis(**session_store)
            self.session_store = RedisSessionStore(self.redis)
        else:
            self.session_store = None
