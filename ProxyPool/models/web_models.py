from abc import ABC

import tornado.web
from tornado import gen

from utils.redis_opt import RedisClient


class GetIndex(tornado.web.RequestHandler, ABC):
    @gen.coroutine
    def get(self):
        self.write("<h2>Welcome to Proxy Pool System</h2>")


class GetProxy(tornado.web.RequestHandler, ABC):
    @gen.coroutine
    def get(self):
        connect = RedisClient()
        self.write(connect.random())


class GetCount(tornado.web.RequestHandler, ABC):
    @gen.coroutine
    def get(self):
        connect = RedisClient()
        self.write(str(connect.count()))
