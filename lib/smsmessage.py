#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
import hashlib
import json
from lib.logger import logger
from config import config

try:
    from config_override import config_override
    config.update(config_override)
except ImportError:
    pass

def lib_send_sms_message(message):
    parse_message = json.loads(message)
    sms_from = parse_message['fromUser']
    sms_to = parse_message['toUser']
    sms_message = parse_message['messageBody'] + config['SMS_SUFFIX']

    sms_data = {
        'username': config['SMS_USERNAME'],
        'password_md5': hashlib.md5( config['SMS_PASSWORD'] ).hexdigest(),
        'apikey': config['SMS_API_KEY'],
        'encode': 'UTF-8',
        'mobile': sms_to,
        'content': sms_message + '【Drchat: ' + sms_from +'】',
    }

    res = requests.post(config['SMS_API_URL'], data = sms_data)

    if res.status_code != 200:
        logger.error('Cannot connect to sms platform: {}'.format(config['SMS_API_URL']) )
        return False

    if res.text.split(':')[0] != 'success':
        logger.error('Send sms error: {}'.format(res.text))
        return False

    logger.debug('Send sms to {} success!'.format(sms_to))
    return True