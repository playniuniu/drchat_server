#!/usr/bin/env python3
# -*- coding: utf-8 -*-
config = {
    # 设置 Server
    'SERVER_HOST' : '0.0.0.0',
    'SERVER_PORT' : 3000,
    'SERVER_TYPE' : 'CLOUD_SERVER',
    # 设置 SocketIO
    'SOCKET_IO_CHANNEL': 'drchat',
    'SOCKET_IO_NAMESPACE' : '/drchat',
    # 设置 Redis
    'REDIS_URL': 'redis://drchat.uunus.cn:6379/0',
    'REDIS_HISTORY_LONG': 1000,
    # 设置 Debug
    'DEBUG_MODE' : 'True',
}
