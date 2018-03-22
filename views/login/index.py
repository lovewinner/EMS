#!/usr/bin/python
# -*- coding: utf-8 -*-

from tornado_lib.routes import route
from views.base_api_handler import BaseAPIHandler as BaseHandler


@route('/login')
class login(BaseHandler):
    def get(self):
        rst = {
            "title": "登录 - "
        }
        self.render('login.html', data = rst)

@route('/logout')
class logout(BaseHandler):
    def get(self):
        rst = {
            "title": "登录 - "
        }
        self.render('login.html', data = rst)