from urllib import quote as url_quote
from tornado.web import HTTPError
import base64

import functools
import urllib
import urlparse
import lib_settings
import logging
# taken from tornado.web.authenticated


def authenticated(method):
    @functools.wraps(method)
    def wrapper(self, *args, **kwargs):
        if not self.current_user:
            #if self.request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            self.set_status(403)
            self.write({
                'error': {
                    'message': 'User unauthorized',
                },
            })
            return 
            """
            if self.request.method in ("GET", "HEAD"):
                url = self.get_login_url()
                if "?" not in url:
                    if urlparse.urlsplit(url).scheme:
                        # if login url is absolute, make next absolute too
                        next_url = self.request.full_url()
                    else:
                        next_url = self.request.uri
                    url += "?" + urllib.urlencode(dict(next=next_url))
                self.redirect(url)
                return
            raise tornado.web.HTTPError(403)
            """
        return method(self, *args, **kwargs)
    return wrapper


def authenticated_plus(extra_check):
    """Decorate methods with this to require that the user be logged in."""
    def wrap(method):
        @functools.wraps(method)
        def wrapper(self, *args, **kwargs):
            if not (self.current_user and extra_check(self.current_user)):
                if self.request.method in ("GET", "HEAD"):
                    url = self.get_login_url()
                    if "?" not in url:
                        if urlparse.urlsplit(url).scheme:
                            # if login url is absolute, make next absolute too
                            next_url = self.request.full_url()
                        else:
                            next_url = self.request.uri
                        url += "?" + urllib.urlencode(dict(next=next_url))
                    self.redirect(url)
                    return
                raise HTTPError(403)
            return method(self, *args, **kwargs)
        return wrapper
    return wrap


def basic_auth(checkfunc, realm="Authentication Required!"):
    """Decorate methods with this to require basic auth"""
    def wrap(method):
        def request_auth(self):
            self.set_header('WWW-Authenticate', 'Basic realm=%s' % realm)
            self.set_status(401)
            self.finish()
            return False
        
        @functools.wraps(method)
        def wrapper(self, *args, **kwargs):
            auth = self.request.headers.get('Authorization')
            if auth is None or not auth.startswith('Basic '):
                return request_auth(self)
            auth = auth[6:]
            try:
                username, password = base64.decodestring(auth).split(':', 2)
            except:
                return request_auth(self)
            
            if checkfunc(username, password):
                self.request.basic_auth = (username, password)
                return method(self, *args, **kwargs)
            else:
                return request_auth(self)
                
        return wrapper
    
    return wrap


def auth_check(method):
    def request_auth_fail(self):
        self.set_status(403)
        self.write("Not Permission")
        self.finish()
        return None

    def check_authentication(self):
        token_key = self.settings.get('request_token_key', 'EdoRequestToken')
        token_value = self.request.headers.get(token_key)
        security_token = self.settings.get('request_security_token', lib_settings.execution_security_token)
        
        if not security_token:
            return {'error_result' : False, 'error_message' : 'Invalid/empty authentication config'}
            
        if security_token and token_value != security_token:
            return {
                    'error_result' : False,
                    'error_message' : "Invalid security token[request_token: %s, excepted: %s]" %
                        (security_token, token_value)
                }
        result = {'error_result' : True, 'error_message' : 'OK'}
        return result

    @functools.wraps(method)
    def wrapper(self, *args, **kwargs):
        
        is_login = False
        ret_ca = {}
        if not is_login :
            ret_ca = check_authentication(self)
            is_login = ret_ca['error_result']
        
        if not is_login :
            logging.warning("Invalid login ret_ca[%s]" % (ret_ca))
            raise HTTPError(403, reason="Invalid auth token")
        
        return method(self, *args, **kwargs)
            
    return wrapper
