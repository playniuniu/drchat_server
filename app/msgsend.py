#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import socket
import socketio
import config
from config import logger

def send_to_socket(msg_type, msg, **kwargs):
    send_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    send_addr = (config.MSG_SEND_IP, config.MSG_SEND_PORT)
    namespace = kwargs.get('namespace', config.SOCKET_IO_NAMESPACE)

    try:
        send_socket.connect(send_addr)
        send_socket.send(msg.encode(encoding='UTF-8'))
        logger.debug("Send msg: {} to {}:{}".format(msg, config.MSG_SEND_IP, config.MSG_SERVER_PORT))
    except:
        logger.error("Send msg to {}:{} error!".format(config.MSG_SEND_IP, config.MSG_SEND_PORT))

    send_socket.close()


def send_to_redis(msg):

    def init_redis():
        redis_mgr = socketio.RedisManager(url=config.REDIS_URL, channel=config.REDIS_CHANNEL, write_only=True)
        sio = socketio.Server(client_manager=redis_mgr)
        return sio

    sio = init_redis()
    sio.emit('msg', msg, namespace=config.SOCKET_IO_NAMESPACE)
    logger.debug("Emit msg: {} success".format(msg))