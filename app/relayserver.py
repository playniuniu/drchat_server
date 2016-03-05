#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import socket
import multiprocessing
import logging
from config import config
from app.msgsend import send_to_redis

try:
    from config_override import config_override
    config.update(config_override)
except ImportError:
    pass

def process_message(sock, addr):
    logging.debug("Process message from {}".format(addr))
    recv_buffer_list = []
    while True:
        recv_buf = sock.recv(1024)
        if recv_buf:
            recv_buffer_list.append(recv_buf)
        else:
            break

    # Close socket
    sock.shutdown(socket.SHUT_WR)
    sock.close()

    # reconstruct message
    recv_message = b''.join(recv_buffer_list)
    recv_message = recv_message.decode('utf-8')
    send_to_redis(recv_message)

def run_relay_server():
    listen_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    listen_socket.bind((config['SERVER_HOST'],config['TCP_SERVER_PORT']))
    listen_socket.listen(5)

    logging.info("Listen on {}:{}".format(config['SERVER_HOST'],config['TCP_SERVER_PORT']))

    while True:
        sock, addr = listen_socket.accept()
        p = multiprocessing.Process(target=process_message, args=(sock, addr))
        p.start()

    listen_socket.close()
