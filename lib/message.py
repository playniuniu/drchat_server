#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import redis
import json
import socketio
from lib.logger import logger
from config import config

try:
    from config_override import config_override
    config.update(config_override)
except ImportError:
    pass

# 将消息推送到 redis queen
def lib_send_redis_message(message, save_flag=True):
    try:
        # connect to the redis queue
        redis = socketio.RedisManager(config['REDIS_REMOTE_URL'], channel=config['SOCKET_IO_CHANNEL'], write_only=True)
        # emit an event
        redis.emit('msg', data=message, namespace=config['SOCKET_IO_NAMESPACE'])
    except:
        logger.error("ERROR! Cannot connect to {}".format(config['REDIS_REMOTE_URL']))
        return False

    if(save_flag):
        lib_save_message_history(message)

# 保存历史消息
def lib_save_message_history(message):
    parse_message = json.loads(message)
    from_user = parse_message['fromUser']
    to_user = parse_message['toUser']

    # 保存两份历史消息, 一份自己用, 一份对方用
    redis_key_local_history = 'msghistory:{}:{}'.format(from_user, to_user)
    redis_key_remote_history = 'msghistory:{}:{}'.format(to_user, from_user)

    # 保存两份消息列表
    redis_key_local_msglist = 'msglist:{}'.format(from_user)
    redis_key_remote_msglist = 'msglist:{}'.format(to_user)

    try:
        redis_client = redis.StrictRedis.from_url(config['REDIS_REMOTE_URL'])

        # 使用 redis 的 mutli 操作
        redis_pipeline = redis_client.pipeline()

        # 保存本地消息
        redis_pipeline.lpush(redis_key_local_history, message)
        redis_pipeline.ltrim(redis_key_local_history, 0, config['REDIS_HISTORY_LONG'])

        # 保存远端消息
        redis_pipeline.lpush(redis_key_remote_history, message)
        redis_pipeline.ltrim(redis_key_remote_history, 0, config['REDIS_HISTORY_LONG'])

        # 保存本地消息列表
        redis_pipeline.hset(redis_key_local_msglist, to_user, message)

        # 保存远端消息列表
        redis_pipeline.hset(redis_key_remote_msglist, from_user, message)

        # 执行所有操作
        redis_pipeline.execute()
    except:
        logger.error("ERROR! Cannot connect to {}".format(config['REDIS_REMOTE_URL']))
        return  False

# 读取历史消息
def lib_get_message_history(from_user, to_user):
    redis_key = 'msghistory:{}:{}'.format(from_user, to_user)
    response = {}

    try:
        redis_client = redis.StrictRedis.from_url(config['REDIS_LOCAL_URL'])
        redis_data = redis_client.lrange(redis_key, 0, config['REDIS_HISTORY_LONG'])
    except:
        logger.error("ERROR! Cannot connect to {}".format(config['REDIS_LOCAL_URL']))
        response['status'] = 'err'
        response['data'] = "连接数据库错误!"
        return response

    response['status'] = 'ok'
    response['data'] = [ el.decode('utf-8') for el in redis_data ]
    return response

# 删除历史消息
def lib_delete_message_history(from_user, to_user):
    redis_key_message_history = 'msghistory:{}:{}'.format(from_user, to_user)
    redis_key_message_list = 'msglist:{}'.format(from_user)
    response = {}

    try:
        redis_client = redis.StrictRedis.from_url(config['REDIS_REMOTE_URL'])

        # 删除历史消息
        redis_client.delete(redis_key_message_history)

        # 删除消息列表
        redis_client.hdel(redis_key_message_list, to_user)
    except:
        logger.error("ERROR! Cannot connect to {}".format(config['REDIS_LOCAL_URL']))
        response['status'] = 'err'
        response['data'] = "连接数据库错误!"
        return response

    response['status'] = 'ok'
    return response

# 获取消息列表
def lib_get_message_list(from_user):
    redis_key = 'msglist:{}'.format(from_user)
    response = {}

    try:
        redis_client = redis.StrictRedis.from_url(config['REDIS_LOCAL_URL'])
        redis_data = redis_client.hvals(redis_key)
    except:
        logger.error("ERROR! Cannot connect to {}".format(config['REDIS_LOCAL_URL']))
        response['status'] = 'err'
        response['data'] = "连接数据库错误!"
        return response

    response['status'] = 'ok'
    response['data'] = [json.loads(el.decode('utf-8')) for el in redis_data]
    return response

# 删除消息列表
def lib_delete_message_list(from_user, to_user):
    redis_key = 'msglist:{}'.format(from_user)
    response = {}

    try:
        redis_client = redis.StrictRedis.from_url(config['REDIS_REMOTE_URL'])
        redis_client.hdel(redis_key, to_user)
    except:
        logger.error("ERROR! Cannot connect to {}".format(config['REDIS_LOCAL_URL']))
        response['status'] = 'err'
        response['data'] = "连接数据库错误!"
        return response

    response['status'] = 'ok'
    return response
