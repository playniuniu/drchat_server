#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import json
from bottle import Bottle, response
import redis
from config import config
import logging

try:
    from config_override import config_override
    config.update(config_override)
except ImportError:
    pass

app = Bottle()

@app.hook('after_request')
def enable_cors():
    """
    You need to add some headers to each request.
    Don't use the wildcard '*' for Access-Control-Allow-Origin in production.
    """
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'PUT, GET, POST, DELETE, OPTIONS'
    response.headers['Access-Control-Allow-Headers'] = 'Origin, Accept, Content-Type, X-Requested-With, X-CSRF-Token'


@app.route('/')
def index():
    response = {
        'description': 'redis message history api server',
        'version': 'v0.1'
    }
    return response

@app.route('/messagelist/<username>')
def messagelist(username):
    messageList = []

    if username == 'drchat':
        messageList.append({'userName': 'aws', 'msgCount': '无消息'})

    elif username == 'aws':
        messageList.append({'userName': 'drchat', 'msgCount': '无消息'})

    else:
        pass

    if messageList:
        response = {
            'status': 'ok',
            'data' : messageList,
        }
    else:
        response = {
            'status': 'err',
            'data' : '没有历史消息',
        }

    return response

@app.route('/contactlist/<username>')
def contactlist(username):
    contactlist = []

    if username == 'drchat':
        contactlist.append({'userName': 'aws'})

    elif username == 'aws':
        contactlist.append({'userName': 'drchat'})

    else:
        pass

    if contactlist:
        response = {
            'status': 'ok',
            'data' : contactlist,
        }
    else:
        response = {
            'status': 'err',
            'data' : '没有联系人信息',
        }

    return response

@app.route('/messages/<fromUser>/<toUser>')
def messages(fromUser, toUser):
    message_key = "{}:msg".format(fromUser)
    try:
        redis_client = redis.StrictRedis.from_url(config['REDIS_URL'])
        message_data = redis_client.lrange(message_key, 0, config['REDIS_HISTORY_LONG'])
    except:
        logging.error("ERROR! Cannot connect to {}".format(config['REDIS_URL']))
        message_data = None


    if message_data:
        message_parse = process_redis_message(message_data, toUser)
        response = {
            'status' : 'ok',
            'data' : message_parse,
        }
        logging.debug("message: {}".format(message_parse))
    else:
        response = {
            'status' : 'error',
            'data' : 'cannot get {}/{} message'.format(fromUser,toUser)
        }
        logging.error('ERROR! Cannot get {}/{} message'.format(fromUser,toUser))

    return response

def process_redis_message(message_data, toUser):
    message_arr = []
    for el in message_data:
        msg = el.decode('utf-8')
        parse_msg = json.loads(msg)
        # 判断收发联系人都一致
        if 'toUser' in parse_msg and parse_msg['toUser'] == toUser:
            message_arr.append(msg)
    return message_arr
