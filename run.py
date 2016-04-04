#!/Users/lele/env/socketio/bin/python3
# -*- coding: utf-8 -*-
from app.sioserver import run_socketio_server
import logging

def main():
    logging.basicConfig(level=logging.DEBUG)
    run_socketio_server()

if __name__ == '__main__':
    main()
