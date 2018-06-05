#!/usr/bin/python
# -*- coding: utf-8 -*-

from tornado_lib.routes import route
from views.base_api_handler import BaseAPIHandler as BaseHandler


@route('/')
class home(BaseHandler):
    def get(self):
        self.render('layout.html', title = "首页 - ")