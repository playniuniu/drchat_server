#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import json
from bottle import Bottle, response, request
import redis
from lib.user import lib_user_login, lib_user_register
from lib.contact import lib_add_contact, lib_get_contact
from config import config
import logging

try:
    from config_override import config_override
    config.update(config_override)
except ImportError:
    pass

app = Bottle()

# 允许跨域访问
@app.hook('after_request')
def enable_cors():
    """
    You need to add some headers to each request.
    Don't use the wildcard '*' for Access-Control-Allow-Origin in production.
    """
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'PUT, GET, POST, DELETE, OPTIONS'
    response.headers['Access-Control-Allow-Headers'] = 'Origin, Accept, Content-Type, X-Requested-With, X-CSRF-Token'

# 主页面
@app.route('/')
def index():
    response = {
        'description': 'drchat api server',
        'version': 'v0.1'
    }
    return json.dumps(response)

# 用户注册
@app.route('/user/register', method='POST')
def post_user_register():
    username = request.forms.get('username')
    password = request.forms.get('password')
    response = lib_user_register(username, password)
    return json.dumps(response)

# 用户登陆
@app.route('/user/login', method='POST')
def post_user_login():
    username = request.forms.get('username')
    password = request.forms.get('password')
    response = lib_user_login(username, password)
    return json.dumps(response)

# 获取联系人信息
@app.route('/contact/<username>', method='GET')
def get_contact(username):
    response = lib_get_contact(username)
    return json.dumps(response)

# 添加联系人信息
@app.route('/contact/<username>', method='POST')
def post_contact(username):
    contact_username = request.forms.get('username')
    contact_nickname = request.forms.get('nickname')
    response = lib_add_contact(username, contact_username, contact_nickname)
    return json.dumps(response)

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
    message_key = "msg:{}:{}".format(fromUser, toUser)
    try:
        redis_client = redis.StrictRedis.from_url(config['REDIS_URL'])
        message_data = redis_client.lrange(message_key, 0, config['REDIS_HISTORY_LONG'])
    except:
        logging.error("ERROR! Cannot connect to {}".format(config['REDIS_URL']))
        message_data = None


    if message_data:
        parse_data = parse_redis_msg(message_data)
        response = {
            'status' : 'ok',
            'data' : parse_data,
        }
        logging.debug("message: {}".format(parse_data))
    else:
        response = {
            'status' : 'error',
            'data' : 'cannot get msg:{}:{} message'.format(fromUser,toUser)
        }
        logging.error('ERROR! Cannot get msg:{}:{} message'.format(fromUser,toUser))

    return response

def parse_redis_msg(message_data):
    message_arr = []
    for el in message_data:
        parse_el = el.decode('utf-8')
        message_arr.append(parse_el)

    return message_arr