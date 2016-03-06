#!/usr/bin/env python3
# -*- coding: utf-8 -*-
config = {
    # 设置 Server
    'SERVER_HOST' : '0.0.0.0',
    # Socket.io 端口
    'MSG_SERVER_PORT' : 3000,
    # 设置消息发送端
    'MSG_SEND_IP' : '127.0.0.1',
    'MSG_SEND_PORT' : 5000,
    # TCP server 端口
    'TCP_SERVER_PORT' : 5000,
    # 设置 Redis
    'REDIS_URL' : 'redis://127.0.0.1:6379/0',
    'REDIS_CHANNEL' : 'drchat',
    'REDIS_HISTORY_LONG' : 1000,
    # 设置 SocketIO namespace
    'SOCKET_IO_NAMESPACE' : '/drchat',
    # 设置 SECRET KEY
    'SECRET_KEY' : 'niuniu@850406',
    # 设置 Debug
    'DEBUG_MODE' : 'True',
}
