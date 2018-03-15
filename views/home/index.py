#!/usr/bin/python
# -*- coding: utf-8 -*-

from tornado_lib.routes import route
from views.base_api_handler import BaseAPIHandler as BaseHandler


@route('/')
class home(BaseHandler):
    def get(self):
        message = self.test("Hello World")

        rst = {
            "title": "This is a test",
            "message": message
        }
        self.render('layout.html', data = rst)