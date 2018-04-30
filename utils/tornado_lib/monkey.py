from gevent import monkey
monkey.patch_all()
import gevent
import threading

from ext.logext import filters
import ext
filters.thread_data = threading.local()
ext.thread_data = filters.thread_data

from tornado.web import Application


class GeventApplication(Application):
    def __call__(self, *args, **kwargs):
        func = super(GeventApplication, self).__call__
        gevent.spawn(func, *args, **kwargs)
