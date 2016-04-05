#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import redis
import json
import socketio
import logging
from config import config

try:
    from config_override import config_override
    config.update(config_override)
except ImportError:
    pass


# 生成历史消息的 redis key
def _message_history_redis_key(message):
    parse_message = json.loads(message)
    from_user = parse_message['fromUser']
    to_user = parse_message['toUser']
    redis_key = 'msghistory:' + min(from_user, to_user) + ":" + max(from_user, to_user)
    return redis_key

# 将消息推送到 redis queen
def lib_send_redis_message(message, save_flag=True):
    try:
        # connect to the redis queue
        redis = socketio.RedisManager(config['REDIS_REMOTE_URL'], channel=config['SOCKET_IO_CHANNEL'], write_only=True)
        # emit an event
        redis.emit('msg', data=message, namespace=config['SOCKET_IO_NAMESPACE'])
        logging.debug("Emit msg: {}".format(message))
    except:
        logging.error("ERROR! Cannot connect to {}".format(config['REDIS_REMOTE_URL']))
        return False

    if(save_flag):
        lib_save_message_history(message)

# 保存历史消息
def lib_save_message_history(message):
    redis_key = _message_history_redis_key(message)

    try:
        redis_client = redis.StrictRedis.from_url(config['REDIS_REMOTE_URL'])
        redis_client.lpush(redis_key, message)
        redis_client.ltrim(redis_key, 0, config['REDIS_HISTORY_LONG'])
    except:
        logging.error("ERROR! Cannot connect to {}".format(config['REDIS_REMOTE_URL']))
        return  False

# 读取历史消息
def lib_get_message_history(from_user, to_user):
    redis_key = 'msghistory:' + min(from_user, to_user) + ":" + max(from_user, to_user)
    response = {}

    try:
        redis_client = redis.StrictRedis.from_url(config['REDIS_LOCAL_URL'])
        redis_data = redis_client.lrange(redis_key, 0, config['REDIS_HISTORY_LONG'])
    except:
        logging.error("ERROR! Cannot connect to {}".format(config['REDIS_LOCAL_URL']))
        response['status'] = 'err'
        response['data'] = "连接数据库错误!"
        return response

    response['status'] = 'ok'
    response['data'] = [ el.decode('utf-8') for el in redis_data ]
    return response