#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import argparse
from app.sioserver import run_socketio_server
from app.relayserver import run_relay_server

def main():
    parser = argparse.ArgumentParser(description='dr chat server')
    parser.add_argument('-t','--type', help='start server type', required=True)
    args = parser.parse_args()

    if args.type == 'sio':
        run_socketio_server()
    elif args.type == 'relay':
        run_relay_server()

if __name__ == '__main__':
    main()
