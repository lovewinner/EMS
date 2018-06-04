#!/user/bin/python
# coding=utf8
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import os
import os.path as osp
import hashlib
from tornado_lib.base import BaseHandler
import logging
import logging.config
import time

PROJECT_ROOT = osp.abspath(osp.dirname(__file__))
PROJECT_NAME = osp.basename(PROJECT_ROOT)

settings = {
    "static_version": str(int(time.time())),
    "static_path": osp.join(PROJECT_ROOT, "static"),
    'static_url_prefix': '/static/',
    'debug': True,
    "cookie_secret": "61oETzKXQAGaYdkL5gEmGeJJFuYh7EQnp2XdTP1o/Vo=",
    "gzip": True,
    'autoescape': 'xhtml_escape',
    'template_path': osp.join(PROJECT_ROOT, "templates"),
    "cache_service": "memcached://127.0.0.1",
    'session_store': {'host': '127.0.0.1'},
    'login_url': '/auth/login',
}

DB_CONFIGURE = [
    {
        "host": '127.0.0.1',
        "port": 3306,
        "username": 'root',
        "password": 'root123',
        "dbname": "EMS",
        "charset": "utf8",
        "is_master": True,
    }
]

DB_CONN_RETRY = 3
