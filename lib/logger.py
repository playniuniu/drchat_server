#!/usr/bin/env python

import logging
from config import config

try:
    from config_override import config_override
    config.update(config_override)
except ImportError:
    pass

LOG_FILE_NAME = config['LOG_FILE_NAME']
LOG_LEVEL = config['LOG_LEVEL']

logger = logging.getLogger('drchat')
logger.setLevel(LOG_LEVEL)
formatter = logging.Formatter('[%(levelname)5s] %(asctime)s - %(filename)s:%(lineno)3d  - %(message)s')

stream_handler = logging.StreamHandler()
stream_handler.setFormatter(formatter)

file_handler = logging.FileHandler(LOG_FILE_NAME,encoding='utf-8')
file_handler.setFormatter(formatter)

logger.addHandler(file_handler)
logger.addHandler(stream_handler)
