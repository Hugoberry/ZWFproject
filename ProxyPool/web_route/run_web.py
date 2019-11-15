import os

import tornado.web
from tornado import ioloop, httpserver
from tornado.web import url

from models.web_models import GetIndex, GetCount, GetProxy


class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            url(r"/", GetIndex),
            url(r"/random", GetProxy),
            url(r"/count", GetCount, name='get_count'),
        ]
        settings = dict(
            template_path=os.path.join(os.path.dirname(__file__), "templates"),
            static_path=os.path.join(os.path.dirname(__file__), "static"),
            debug=False,
        )
        tornado.web.Application.__init__(self, handlers, **settings)


if __name__ == "__main__":
    application = httpserver.HTTPServer(Application())
    application.listen(8848)
    tornado.ioloop.IOLoop.current().start()
