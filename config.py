#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import logging

# 设置平台属性 SERVER/CLIENT
PLATFORM = 'SERVER'

# 设置 Server
SERVER_HOST = '0.0.0.0'

# Socket.io 端口
MSG_SERVER_PORT = 3000

if PLATFORM == 'SERVER':
    # 设置消息发送端
    MSG_SEND_IP = '127.0.0.1'
    MSG_SEND_PORT = 5000

    # TCP server 端口
    TCP_SERVER_PORT = 4001

else:
    # 设置消息发送端
    MSG_SEND_IP = '127.0.0.1'
    MSG_SEND_PORT = 4000

    # TCP server 端口
    TCP_SERVER_PORT = 5001


# 设置 Redis
REDIS_URL = 'redis://127.0.0.1:6379/0'
REDIS_CHANNEL = 'drchat'

# 设置 SocketIO namespace
SOCKET_IO_NAMESPACE = '/drchat'

# 设置 SECRET KEY
SECRET_KEY = 'niuniu@850406'

# 设置 Debug
DEBUG_MODE = True

# 设置 Logger
if DEBUG_MODE:
    logging.basicConfig(level=logging.DEBUG)
else:
    logging.basicConfig(level=logging.INFO)

logger = logging.getLogger('DRCHATSERVER')
