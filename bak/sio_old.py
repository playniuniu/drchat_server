#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import logging
import eventlet
from flask import Flask
from flask_socketio import SocketIO, emit
import config

# Setting logger
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Setting eventlet
eventlet.monkey_patch()

# Setting socket-io
app = Flask(__name__)
app.config['SECRET_KEY'] = config.SECRET_KEY

socketio_app = SocketIO(app, async_mode='eventlet', message_queue=config.REDIS_URL, channel=config.REDIS_CHANNEL)

socketio_namespace = config.SOCKET_IO_NAMESPACE

@socketio_app.on('connect', namespace=socketio_namespace)
def socketio_connect():
    logger.debug("User connect")

@socketio_app.on('join', namespace=socketio_namespace)
def socketio_join(message):
    logger.debug("User join")

@socketio_app.on('disconnect', namespace=socketio_namespace)
def socketio_disconnect():
    logger.debug("User disconnect")

@socketio_app.on('msg', namespace=socketio_namespace)
def socketio_chat(message):
    logger.debug("Recv msg: {}".format(message))
    emit('msg', message,  broadcast=True)

def run_socketio_server():
    logger.info("Socketio server run on host:{}, port:{}".format(config.SERVER_HOST, config.MSG_SERVER_PORT))
    socketio_app.run(app, host=config.SERVER_HOST, port=config.MSG_SERVER_PORT)
