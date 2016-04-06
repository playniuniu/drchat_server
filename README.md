# Drchat

### 简介

Drchat 共分成2个部分，一部分是 Server 端，一部分是 Client 端，共同完成一个基于微信通信的聊天软件

### Client 端
[Client](https://github.com/playniuniu/drchat_client) 端采用 [Framework7](http://framework7.taobao.org) 做为界面，采用 [Socket.io](http://socket.io) 做 Websocket，实现通信

### Server 端

[Server](https://github.com/playniuniu/drchat_server) 端采用 [python-socketio](https://python-socketio.readthedocs.org) 作为 Server，后台使用了 [redis](http://redis.io/) 支撑消息服务, 详细说明见 [这里](http://socket.io/docs/rooms-and-namespaces/#sending-messages-from-the-outside-world), 对于 python-socketio 参见 [这里](http://python-socketio.readthedocs.org/)

### 系统架构
![系统架构](arch.png)

这里有一下几点需要注意：

- 整个后台的 Redis 服务，由云端 redis 支撑，其余所有 redis 都与其同步
- socketio server 负责从 redis 读取消息并发送用户
- socketio server 同时包含了一个 REST API，用于用户登录，消息记录等

### Server 端安装

本程序采用 Python3, 先安装 redis， 再使用 ```pip install -r requirements.txt``` 即可

### 使用

- redis 设置主从模式，从 redis.conf 中设置 slaveof cloudip 6639
- 开启 sockeio server ```./run.py```


