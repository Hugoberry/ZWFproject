import tornado.web
from tornado import gen

from APPS.utils.hbase_test import get_hbase


class GetIndex(tornado.web.RequestHandler):
    @gen.coroutine
    def get(self):
        self.render("index.html")


class GetHbase(tornado.web.RequestHandler):
    @gen.coroutine
    def get(self):
        res = yield gen.convert_yielded(get_hbase(page=1))
        self.render("grids.html", res=res)

    @gen.coroutine
    def post(self):
        page = self.get_argument("page", default="1")
        res = yield gen.convert_yielded(get_hbase(page=page))
        self.render("grids.html", res=res)


class Get404(tornado.web.RequestHandler):
    @gen.coroutine
    def get(self):
        self.render("404.html")