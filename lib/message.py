#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import socketio
import logging
from config import config

try:
    from config_override import config_override
    config.update(config_override)
except ImportError:
    pass


def lib_send_redis_message(message):
    try:
        # connect to the redis queue through RedisManager
        redis = socketio.RedisManager(config['REDIS_URL'], channel=config['SOCKET_IO_CHANNEL'], write_only=True)
    except:
        logging.error("ERROR! Cannot connect to {}".format(config['REDIS_URL']))
        return False

    # emit an event
    redis.emit('msg', data=message, namespace=config['SOCKET_IO_NAMESPACE'])
    logging.debug("Emit msg: {}".format(message))