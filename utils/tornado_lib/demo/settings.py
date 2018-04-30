#!/user/bin/python
# coding=utf8
import os
import os.path as osp
import hashlib
import logging
from tornado_lib.base import BaseHandler
from ext import setup_logger

PROJECT_ROOT = osp.abspath(osp.dirname(__file__))
PROJECT_NAME = osp.basename(PROJECT_ROOT)

settings = {
    'debug': True,
    "static_path": osp.join(PROJECT_ROOT, "static"),
    'static_url_prefix': '/static/',

    "cookie_secret": hashlib.md5("61oETzKXQAGaYdkL5gEmGeJJFuYh7EQnp2XdTP1o/Vo=" + PROJECT_NAME).hexdigest(),
    "xsrf_cookies": False,
    "gzip": True,
    'autoescape': 'xhtml_escape',
    'template_path': osp.join(PROJECT_ROOT, "templates"),
    'log_function': BaseHandler.log_function,
}

setup_logger()
