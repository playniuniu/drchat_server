import redis
import logging
import json
from config import config

try:
    from config_override import config_override
    config.update(config_override)
except ImportError:
    pass

# 添加联系人
def lib_add_contact(username, contact_username, contact_nickname):
    hash_key = 'contact:' + username
    response = {}

    params = {
        'username' : contact_username,
        'nickname' : contact_nickname
    }

    try:
        redis_client = redis.StrictRedis.from_url(config['REDIS_URL'])
        redis_client.hset(hash_key, contact_username, json.dumps(params))
    except:
        logging.error("ERROR! Cannot connect to {}".format(config['REDIS_URL']))
        response['status'] = 'err'
        response['data'] = "连接数据库错误!"
        return response

    logging.debug("Success add contact {} to user {}".format(contact_username, username))
    response['status'] = 'ok'
    return response

# 列出联系人列表
def lib_get_contact(username):
    hash_key = 'contact:' + username
    response = {}

    try:
        redis_client = redis.StrictRedis.from_url(config['REDIS_URL'])
        redis_data = redis_client.hvals(hash_key)
    except:
        logging.error("ERROR! Cannot connect to {}".format(config['REDIS_URL']))
        response['status'] = 'err'
        response['data'] = "连接数据库错误!"
        return response

    response['status'] = 'ok'
    response['data'] = [ json.loads(el.decode('utf-8')) for el in redis_data ]
    return response