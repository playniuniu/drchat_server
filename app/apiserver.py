#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from tornado.web import RequestHandler, Application
import tornado.wsgi
import redis
from config import config
import logging

try:
    from config_override import config_override
    config.update(config_override)
except ImportError:
    pass

class MainHandler(RequestHandler):
    def get(self):
        response = {
            'description': 'redis message history api server',
            'version': 'v0.1'
        }
        self.write(response)

class MessageHandler(RequestHandler):
    def get(self, username):
        message_key = "{}:msg".format(username)
        try:
            redis_client = redis.StrictRedis.from_url(config['REDIS_URL'])
            message_data = redis_client.lrange(message_key, 0, config['REDIS_HISTORY_LONG'])
        except:
            logging.error("ERROR! Cannot connect to {}".format(config['REDIS_URL']))
            message_data = None


        if message_data:
            message_parse = process_redis_message(message_data)
            response = {
                'status' : 'ok',
                'data' : message_parse,
            }
            logging.debug("message: {}".format(message_parse))
        else:
            response = {
                'status' : 'error',
                'data' : 'cannot get {} message'.format(username)
            }
            logging.error('ERROR! Cannot get {} message'.format(username))

        self.write(response)

        # 允许跨域访问
        self.set_header('Access-Control-Allow-Origin', '*')
        self.set_header('Access-Control-Allow-Methods', 'POST, GET, UPDATE, DELETE, OPTIONS')
        self.set_header('Access-Control-Max-Age', 1728000)
        self.set_header('Access-Control-Allow-Headers', '*')


def process_redis_message(message_data):
    message_arr = []
    for el in message_data:
        message_arr.append(el.decode('utf-8'))
    return message_arr

application = Application([
    (r"/", MainHandler),
    (r"/message/(\w+)", MessageHandler),
])

apiserver = tornado.wsgi.WSGIAdapter(application)
