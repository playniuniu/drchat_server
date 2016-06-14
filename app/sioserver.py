#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import json
import socketio
import eventlet
from eventlet import wsgi
from config import config
from app.apiserver import app
from lib.logger import logger
from lib.message import lib_send_redis_message
from lib.smsmessage import lib_send_sms_message

try:
    from config_override import config_override
    config.update(config_override)
except ImportError:
    pass

def init_redis_io():
    # Setting eventlet, important
    eventlet.monkey_patch()

    # Set redis manager
    redis_mgr = socketio.RedisManager(url=config['REDIS_LOCAL_URL'], channel=config['SOCKET_IO_CHANNEL'])

    # Setting socket-io
    socket_io = socketio.Server(client_manager=redis_mgr)

    return socket_io

def init_sio():
    sio = init_redis_io()

    # Setting namespace
    socketio_namespace = config['SOCKET_IO_NAMESPACE']

    # Setting socket io event
    @sio.on('connect', namespace=socketio_namespace)
    def connect(sid, environ):
        logger.debug('user connect {}'.format(sid))

    @sio.on('disconnect', namespace=socketio_namespace)
    def disconnect(sid):
        logger.debug('user disconnect {}'.format(sid))

    @sio.on('enter room', namespace=socketio_namespace)
    def enter_room(sid, data):
        sio.enter_room(sid, data['room'])

    @sio.on('leave room', namespace=socketio_namespace)
    def leave_room(sid, data):
        sio.leave_room(sid, data['room'])

    # Process socket io msg
    @sio.on('msg', namespace=socketio_namespace)
    def process_message(sid, data):
        logger.debug('process message: {}'.format(data))

        # Send to redis message queen
        lib_send_redis_message(data)

        # TODO: need to reconstruct to use cloud server to send sms message
        # Send to sms
        parse_data = json.loads(data)
        if config['SERVER_TYPE'] == 'LOCAL' and parse_data['sendSmsFlag']:
            lib_send_sms_message(data)

    return sio

def run_socketio_server():
    logger.info("Socketio server run on host:{}, port:{}".format(config['SERVER_HOST'], config['SERVER_PORT']))
    sio = init_sio()
    hybrid_server = socketio.Middleware(sio, app)
    eventlet_socket = eventlet.listen(('', config['SERVER_PORT']))
    wsgi.server(eventlet_socket, hybrid_server)
