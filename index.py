#!/usr/bin/python
# -*- coding: utf-8 -*-

import views
import tornado.web
import logging

from settings import settings
from tornado_lib.routes import route
from tornado_lib.base import SessionApplication

urls = route.get_routes()
app = SessionApplication(urls, **settings)

if __name__ == '__main__':
    from tornado.options import define, parse_command_line, options
    define("port", type = int, default = 8001, help = "Server port")
    define("address", type = str, default = '127.0.0.1', help = "Server Address")
    parse_command_line()

    app.listen(options.port, options.address, xheaders = True)
    logging.info('Server is Runing... %s ', options.port)
    tornado.ioloop.IOLoop.instance().start()