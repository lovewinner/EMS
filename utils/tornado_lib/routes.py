# The route helpers were originally written by
# Jeremy Kelley (http://github.com/nod).
import inspect
from collections import OrderedDict
import os.path as osp

import tornado.web


class route(object):
    """
    decorates RequestHandlers and builds up a list of routables handlers

    Tech Notes (or 'What the *@# is really happening here?')
    --------------------------------------------------------

    Everytime @route('...') is called, we instantiate a new route object which
    saves off the passed in URI.  Then, since it's a decorator, the function is
    passed to the route.__call__ method as an argument.  We save a reference to
    that handler with our uri in our class level routes list then return that
    class to be instantiated as normal.

    Later, we can call the classmethod route.get_routes to return that list of
    tuples which can be handed directly to the tornado.web.Application
    instantiation.

    Example
    -------

    @route('/some/path')
    class SomeRequestHandler(RequestHandler):
        pass

    @route('/some/path', name='other')
    class SomeOtherRequestHandler(RequestHandler):
        pass

    my_routes = route.get_routes()
    """
    _routes = OrderedDict()

    def __init__(self, uri, name=None):
        self._uri = uri
        self.name = name

    def __call__(self, _handler):
        """gets called when we class decorate"""
        name = self.name and self.name or _handler.__name__
        name = name.lower()
        self._routes.setdefault(_handler, [])
        self._routes[_handler].append(tornado.web.url(
            self._uri, _handler, name=name
        ))
        return _handler

    @classmethod
    def get_routes(self):
        urls = []
        for url_list in self._routes.values():
            urls.extend(url_list)
        return urls


def route_redirect(from_, to, name=None):
    route._routes[object()] = [tornado.web.url(
        from_, tornado.web.RedirectHandler, dict(url=to), name=name
    )]


def _get_url_name(name):
    n = []
    for x in name:
        if x >= 'A' and x <= 'Z':
            n.append('_')
        n.append(x)
    n = ''.join(n)
    return n.strip('_').lower()


def handler_to_url(handler):
    abspath = osp.abspath(inspect.getsourcefile(handler)).lower()
    abspath = abspath.replace('\\', '/')
    if not handler.VIEWS_ROOT:
        view_root = abspath
        while True:
            if osp.basename(view_root) == 'views':
                break
            view_root = osp.dirname(view_root)
            if not view_root or view_root == '/':
                return None
    else:
        view_root = handler.VIEWS_ROOT
        view_root = view_root.rstrip('/')
    view_root = osp.abspath(view_root)
    view_root = view_root.replace('\\', '/')
    abspath = abspath.replace(view_root, '')

    filename = osp.splitext(abspath)[0]

    url_name = _get_url_name(handler.__name__)
    if url_name == 'index':
        url_name = ''
    s = '%s/%s' % (filename, url_name)
    s = s.rstrip('/')
    return s


class UrlHandlerType(type):
    def __new__(cls, name, bases, dct):
        res = type.__new__(cls, name, bases, dct)
        if not issubclass(res, tornado.web.RequestHandler):
            return res
        name = name.lower()
        if name not in ('requesthandler', 'basehandler') and \
                not name.startswith('base') and not name.startswith('_'):
            url = handler_to_url(res)
            if url:
                route(url)(res)
        return res


class UrlHandler(object):
    __metaclass__ = UrlHandlerType
    VIEWS_ROOT = None
    pass


@route('/nginx_status_rand.*')
class StatusCheck(tornado.web.RequestHandler):
    def get(self):
        self.write('OK')
    post = get


if __name__ == '__main__':
    class AA(tornado.web.RequestHandler, UrlHandler):
        def get(self):
            pass

    @route('/test')
    class B(tornado.web.RequestHandler, UrlHandler):
        def get(self):
            pass

    print route.get_routes()
