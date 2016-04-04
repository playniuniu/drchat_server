#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import socketio
import logging
import eventlet
from eventlet import wsgi
from config import config
from lib.message import save_message
from app.apiserver import app

try:
    from config_override import config_override
    config.update(config_override)
except ImportError:
    pass

def init_redis():
    # Setting eventlet, important
    eventlet.monkey_patch()

    # Set redis manager
    redis_mgr = socketio.RedisManager(url=config['REDIS_URL'], channel=config['SOCKET_IO_CHANNEL'])

    # Setting socket-io
    sio = socketio.Server(client_manager=redis_mgr)

    return sio

def init_sio():
    sio = init_redis()

    # Setting namespace
    socketio_namespace = config['SOCKET_IO_NAMESPACE']

    # Setting socket io event
    @sio.on('connect', namespace=socketio_namespace)
    def connect(sid, environ):
        logging.debug('user connect {}'.format(sid))

    @sio.on('disconnect', namespace=socketio_namespace)
    def disconnect(sid):
        logging.debug('user disconnect {}'.format(sid))

    @sio.on('enter room', namespace=socketio_namespace)
    def enter_room(sid, data):
        sio.enter_room(sid, data['room'])

    @sio.on('leave room', namespace=socketio_namespace)
    def leave_room(sid, data):
        sio.leave_room(sid, data['room'])

    # Process socket io msg
    @sio.on('msg', namespace=socketio_namespace)
    def process_message(sid, data):
        logging.debug('message {}'.format(data))
        # Send to local web server
        # sio.emit('msg', data, namespace=socketio_namespace, skip_sid=sid)

        # save history message to redis
        save_message(data, 'send')

    return sio

def run_socketio_server():
    logging.info("Socketio server run on host:{}, port:{}".format(config['SERVER_HOST'], config['SERVER_PORT']))
    sio = init_sio()
    hybrid_server = socketio.Middleware(sio, app)
    eventlet_socket = eventlet.listen(('', config['SERVER_PORT']))
    wsgi.server(eventlet_socket, hybrid_server)
