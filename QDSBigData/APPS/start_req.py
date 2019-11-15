import os

import tornado.web
from tornado import ioloop, httpserver
from tornado.web import url

from APPS.models.some_model import GetHbase, GetIndex, Get404


class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            url(r"/", GetIndex),
            url(r"/get_hbase", GetHbase),
            url(r"/get404", Get404, name='get404'),
        ]
        settings = dict(
            template_path=os.path.join(os.path.dirname(__file__), "templates"),
            static_path=os.path.join(os.path.dirname(__file__), "static"),
            debug=False,
        )
        tornado.web.Application.__init__(self, handlers, **settings)


if __name__ == "__main__":
    application = httpserver.HTTPServer(Application())
    application.listen(80)
    tornado.ioloop.IOLoop.current().start()
