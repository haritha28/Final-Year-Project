import tornado.options
import tornado.web
from async_psycopg2 import Pool

import tornado.ioloop
from tornado import gen
import asyncmc
import momoko

loop = ''
memcache = ''


class BaseHandler(tornado.web.RequestHandler):
    @property
    def db(self):
        if not self.application.db:
            self.application.db = Pool(1, 10, 10, **{
                'host': '127.0.0.1',
                'database': "ashaDB",
                'user': "postgres",
                'password': "amma123",
                'async': 1
            })
        return self.application.db

    def get_current_user(self):
        return self.get_secure_cookie("user")


@gen.coroutine
def instantiate():
    db = Pool(1, 10, 10, **{
        'host': 'localhost',
                'database': 'ashaDB',
                'user': 'postgres',
                'password': 'amma123',
                'async': 1
    })
