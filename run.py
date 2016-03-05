#!/Users/lele/env/socketio/bin/python3
# -*- coding: utf-8 -*-
import argparse
from app.sioserver import run_socketio_server
from app.relayserver import run_relay_server
import logging

def main():

    logging.basicConfig(level=logging.DEBUG)

    parser = argparse.ArgumentParser(description='dr chat server')
    parser.add_argument('type', help='server type, sio | relay')
    args = parser.parse_args()

    if args.type == 'sio':
        run_socketio_server()
    elif args.type == 'relay':
        run_relay_server()
    else:
        print("server type error!")
        exit(1)

if __name__ == '__main__':
    main()
