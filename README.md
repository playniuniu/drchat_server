# Drchat

### 简介

Drchat 共分成2个部分，一部分是 Server 端，一部分是 Client 端，共同完成一个基于微信通信的聊天软件

### Client 端
[Client](https://github.com/playniuniu/drchat_client) 端采用 [Framework7](http://framework7.taobao.org) 做为界面，采用 [Socket.io](http://socket.io) 做 Websocket，实现通信

### Server 端

[Server](https://github.com/playniuniu/drchat_server) 端采用 [python-socketio](https://python-socketio.readthedocs.org) 作为 Server，并自建了一个 TCP Server 用于监听从卫星传回的消息。

这里有一下几点需要注意：

- 整个信息的后台，存入 Redis 数据库，以实现 socketio 与 tcpserver 的信息共享
- socketio 的 Server 只负责从 redis 读取消息，并向 Web 端吐消息
- tcpserver 只负责从网络监听消息，并向 redis 存入消息

### Server 端安装

本程序采用 Python3, 使用 pip install -r requirements.txt 即可

### 使用

- 本程序需同时开启 sockeio 和 tcpserver
- 开启 sockeio ```run.py -t sio```
- 开启 tcpserver ```run.py -t relay```

