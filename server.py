# -*- coding: utf-8 -*-
import tornado.web
import tornado.ioloop
import config
import urls
import tornado.options
from tornado.options import options, parse_command_line,define
define("port", default=8000, type=int, help="run server on the given port.")

if __name__ == '__main__':
    options.log_file_prefix = config.log_path
    options.logging = config.log_level
    tornado.options.parse_command_line()
    app=urls.BaseApplication()
    app.listen(options.port,'192.168.230.129')
    tornado.ioloop.IOLoop.current().start()
