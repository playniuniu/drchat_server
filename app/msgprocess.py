#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import socket
import socketio
import logging
from config import config

try:
    from config_override import config_override
    config.update(config_override)
except ImportError:
    pass


# 将单个JSON数据放入数组中,并打包
# JSON -> [ Dict ]
def construct_msg(msg):
    if msg is None:
        return None
    try:
        msg_arr = []
        msg_arr.append(json.loads(msg))
        return msg_arr
    except:
        logging.error("ERROR! construct message error: {}".format(msg))
        return None

# 将多个JSON解包后放入数组中
# JSON_ARR -> [ Dict, Dict, Dict ]
def deconstruct_msg(msg):
    if msg is None:
        return None

    try:
        parse_msg = json.loads(msg)
        msg_arr = []
        for el in parse_msg:
            msg_arr.append(el)
        return msg_arr
    except:
        logging.error("ERROR! deconstruct message error: {}".format(msg))
        return None

def send_to_socket(msg_type, msg, **kwargs):
    send_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    send_addr = (config['MSG_SEND_IP'], config['MSG_SEND_PORT'])
    namespace = kwargs.get('namespace', config['SOCKET_IO_NAMESPACE'])

    # 将单条消息放入数组, 为后续兼容准备
    send_msg = construct_msg(msg)

    if send_msg is None:
        return

    try:
        send_socket.connect(send_addr)
        send_socket.send(json.dumps(send_msg).encode(encoding='UTF-8'))
        logging.debug("Send msg to {}:{}".format(config['MSG_SEND_IP'], config['MSG_SERVER_PORT']))
    except:
        logging.error("Send msg to {}:{} error!".format(config['MSG_SEND_IP'], config['MSG_SEND_PORT']))

    send_socket.close()


def send_to_redis(msg):

    def init_redis():
        redis_mgr = socketio.RedisManager(url=config['REDIS_URL'], channel=config['REDIS_CHANNEL'], write_only=True)
        sio = socketio.Server(client_manager=redis_mgr)
        return sio

    sio = init_redis()

    # 对于接收数据, 需要先行解包,然后依次放入
    message_arr = deconstruct_msg(msg)
    if message_arr is None:
        return

    for el in message_arr:
        sio.emit('msg', json.dumps(el), namespace=config['SOCKET_IO_NAMESPACE'])
        logging.debug("Emit msg: {} success".format(el))


def save_message(msg, message_type):
    try:
        redis_mgr = socketio.RedisManager(url=config['REDIS_URL'], channel=config['REDIS_CHANNEL'], write_only=True)
        redis_client = redis_mgr.redis

        # toUser 和 fromUser 需要参考前端的 API
        # 对于接收数据, 需要先行解包,然后依次放入
        if message_type == 'receive' :
            message_arr = deconstruct_msg(msg)

            for el in message_arr:
                # 存入的数据以 msg:本地:远端 为格式
                save_key = "msg:{}:{}".format(el['toUser'], el['fromUser'])
                redis_client.lpush(save_key, json.dumps(el))
                redis_client.ltrim(save_key, 0, config['REDIS_HISTORY_LONG'])
        else:
            # 对于发送数据, 直接存入数据库
            parse_msg = json.loads(msg)

            # 存入的数据以 msg:本地:远端 为格式
            save_key = "msg:{}:{}".format(parse_msg['fromUser'], parse_msg['toUser'])
            redis_client.lpush(save_key, msg)
            redis_client.ltrim(save_key, 0, config['REDIS_HISTORY_LONG'])
    except:
        logging.error("Cannot save history message to redis")
