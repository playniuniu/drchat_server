#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import redis
import logging
import json
from config import config

try:
    from config_override import config_override
    config.update(config_override)
except ImportError:
    pass

# 用户注册
def lib_user_register(username, password):
    hash_key = 'user'
    response = {}

    try:
        redis_client = redis.StrictRedis.from_url(config['REDIS_REMOTE_URL'])
        redis_data = redis_client.hget(hash_key, username)
    except:
        logging.error("ERROR! Cannot connect to {}".format(config['REDIS_REMOTE_URL']))
        response['status'] = 'err'
        response['data'] = "连接数据库错误!"
        return response

    if redis_data:
        logging.warning("WARNING! User {} already exist".format(username))
        response['status'] = 'err'
        response['data'] = "用户已被注册!"
        return response

    save_data = {
        'username' : username,
        'password' : password,
    }

    redis_client.hset(hash_key, username, json.dumps(save_data))
    logging.debug("Success register user {}".format(username))
    response['status'] = 'ok'
    response['data'] = { "username" : username }
    return response

# 用户登陆
def lib_user_login(username, password):
    hash_key = 'user'
    response = {}

    try:
        redis_client = redis.StrictRedis.from_url(config['REDIS_LOCAL_URL'])
        redis_data = redis_client.hget(hash_key, username)
    except:
        logging.error("ERROR! Cannot connect to {}".format(config['REDIS_LOCAL_URL']))
        response['status'] = 'err'
        response['data'] = "连接数据库错误!"
        return response

    if redis_data is None:
        logging.warning("WARNING! User {} not exist".format(username))
        response['status'] = 'err'
        response['data'] = "该用户尚未注册!"
        return response

    user_data = json.loads(redis_data.decode('utf-8'))

    if user_data['password'] != password:
        logging.debug("User {} password is not correct".format(username))
        response['status'] = 'err'
        response['data'] = "密码错误!"
    else:
        logging.debug("User {} login success".format(username))
        response['status'] = 'ok'
        response['data'] = {"username": username}
    return response
