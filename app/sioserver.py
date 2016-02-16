#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import socketio
import eventlet
from eventlet import wsgi
import config
from config import logger
from app.msgsend import send_to_socket

def init_redis():
    # Setting eventlet, important
    eventlet.monkey_patch()

    # Set redis manager
    redis_mgr = socketio.RedisManager(url=config.REDIS_URL, channel=config.REDIS_CHANNEL)

    # Setting socket-io
    sio = socketio.Server(client_manager=redis_mgr)

    return sio

def init_sio():
    sio = init_redis()

    # Setting namespace
    socketio_namespace = config.SOCKET_IO_NAMESPACE

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
        logger.debug('message {}'.format(data))
        # Send to local web server
        sio.emit('msg', data, namespace=socketio_namespace, skip_sid=sid)
        # Send to socket
        send_to_socket('msg', data, namespace=socketio_namespace)

    return sio

def run_socketio_server():
    logger.info("Socketio server run on host:{}, port:{}".format(config.SERVER_HOST, config.FLASK_PORT))
    sio = init_sio()
    app = socketio.Middleware(sio)
    eventlet_socket = eventlet.listen(('', config.FLASK_PORT))
    wsgi.server(eventlet_socket, app)
