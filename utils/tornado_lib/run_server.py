#!/usr/bin/python
#coding=utf8
import logging
import tornado.ioloop
from tornado.options import define, parse_command_line, options

define("port", type=int, default=9000,
       help="the server port")
define("address", type=str, default='0.0.0.0',
       help="the server address")


def parse_options():
    parse_command_line()
    return options


def run_server(app):
    app.listen(options.port, options.address, xheaders=True)
    logging.info('start debug server %s:%s', options.address, options.port)
    tornado.ioloop.IOLoop.instance().start()

