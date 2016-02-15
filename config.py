#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import logging

# 设置 SECRET KEY
SECRET_KEY = 'niuniu@850406'

# 设置 Flask Server
SERVER_HOST = '0.0.0.0'
FLASK_PORT = 3000
RELAY_PORT = 3002

# 设置 Redis
REDIS_URL = 'redis://127.0.0.1:6379/0'
REDIS_CHANNEL = 'drchat'

# 设置 SocketIO
SOCKET_IO_NAMESPACE = '/drchat'

# 设置 Relay client
REMOTE_RELAY_IP = '127.0.0.1'
REMOTE_RELAY_PORT = 3002

# 设置 Debug
DEBUG_MODE = True

# 设置 Logger
if DEBUG_MODE:
    logging.basicConfig(level=logging.DEBUG)
else:
    logging.basicConfig(level=logging.INFO)

logger = logging.getLogger('DRCHATSERVER')

