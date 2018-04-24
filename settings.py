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
import lib_settings
import time
from ext import setup_logger

PROJECT_ROOT = osp.abspath(osp.dirname(__file__))
PROJECT_NAME = osp.basename(PROJECT_ROOT)

DB_HOST = '127.0.0.1'
DB_USERNAME = 'root'
DB_PASSWORD = 'root123'

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

ACCOUNT_DB_LIST = {
    "host": DB_HOST,
    "port": 3306,
    "username": DB_USERNAME,
    "password": DB_PASSWORD,
    "dbname": "account",
    'charset': "utf8",
}

EXPERIMENT_DB_LIST = {
    "host": DB_HOST,
    "port": 3306,
    "username": DB_USERNAME,
    "password": DB_PASSWORD,
    "dbname": "experiment",
    'charset': "utf8",
}

EXPERIMENT_BOOK_DB_LIST = {
    "host": DB_HOST,
    "port": 3306,
    "username": DB_USERNAME,
    "password": DB_PASSWORD,
    "dbname": "experiment_book",
    'charset': "utf8",
}

EXPERIMENT_PUBLISH_DB_LIST = {
    "host": DB_HOST,
    "port": 3306,
    "username": DB_USERNAME,
    "password": DB_PASSWORD,
    "dbname": "experiment_publish",
    'charset': "utf8",
}
