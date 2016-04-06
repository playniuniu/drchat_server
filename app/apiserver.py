#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import json
from bottle import Bottle, response, request
from lib.user import lib_user_login, lib_user_register
from lib.contact import lib_add_contact, lib_get_contact, lib_delete_contact
from lib.message import lib_get_message_history, lib_delete_message_history, \
    lib_get_message_list, lib_delete_message_list

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
@app.route('/contact/<username>',  method=['OPTIONS', 'PUT'])
def update_contact(username):
    # 处理跨域访问中, 先发送 OPTIONS 的问题
    if request.method == 'OPTIONS':
        return {}

    contact_username = request.params.get('username')
    contact_nickname = request.params.get('nickname')
    response = lib_add_contact(username, contact_username, contact_nickname)
    return json.dumps(response)

# 删除联系人信息
@app.route('/contact/<username>',  method=['OPTIONS', 'DELETE'])
def delete_contact(username):
    # 处理跨域访问中, 先发送 OPTIONS 的问题
    if request.method == 'OPTIONS':
        return {}

    contact_username = request.params.get('username')
    response = lib_delete_contact(username, contact_username)
    return json.dumps(response)

# 获取联系人消息列表
@app.route('/msglist/<username>', method='GET')
def get_message_list(username):
    pass

# 获取历史消息
@app.route('/msghistory/<fromUser>/<toUser>', method='GET')
def get_message_history(fromUser, toUser):
    return lib_get_message_history(fromUser, toUser)

# 删除历史消息
@app.route('/msghistory/<fromUser>/<toUser>', method=['OPTIONS', 'DELETE'])
def delete_message_history(fromUser, toUser):
    # 处理跨域访问中, 先发送 OPTIONS 的问题
    if request.method == 'OPTIONS':
        return {}

    return lib_delete_message_history(fromUser, toUser)

# 获取消息列表
@app.route('/msglist/<fromUser>', method='GET')
def get_message_list(fromUser):
    return lib_get_message_list(fromUser)

# 删除历史消息
@app.route('/msglist/<fromUser>', method=['OPTIONS', 'DELETE'])
def delete_message_list(fromUser):
    # 处理跨域访问中, 先发送 OPTIONS 的问题
    if request.method == 'OPTIONS':
        return {}

    toUser = request.params.get('username')
    return lib_delete_message_list(fromUser, toUser)
