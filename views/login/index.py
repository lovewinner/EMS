#!/usr/bin/python
# -*- coding: utf-8 -*-

from tornado_lib.routes import route
from views.base_api_handler import BaseAPIHandler as BaseHandler


@route('/auth/login')
class login(BaseHandler):
    def get(self):
        self.render('index.html', title="This is a test")