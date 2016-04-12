#!/usr/bin/env python3
# -*- coding: utf-8 -*-
config = {
    # 设置 Server
    'SERVER_HOST' : '0.0.0.0',
    'SERVER_PORT' : 3000,
    # 设置 SocketIO
    'SOCKET_IO_CHANNEL': 'drchat',
    'SOCKET_IO_NAMESPACE' : '/drchat',
    # 设置 Redis
    'REDIS_LOCAL_URL': 'redis://:dr123456@127.0.0.1:6379/0', # 本地 redis
    'REDIS_REMOTE_URL': 'redis://:dr123456@drchat.uunus.cn:6379/0',  # 云端 redis
    'REDIS_HISTORY_LONG': 1000,
    # 设置 Debug
    'DEBUG_MODE' : 'True',
}
