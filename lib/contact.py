import redis
import json
from lib.logger import logger
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
        redis_client = redis.StrictRedis.from_url(config['REDIS_REMOTE_URL'])
        redis_client.hset(hash_key, contact_username, json.dumps(params))
    except:
        logger.error("ERROR! Cannot connect to {}".format(config['REDIS_REMOTE_URL']))
        response['status'] = 'err'
        response['data'] = "连接数据库错误!"
        return response

    logger.debug("Success add contact {} to user {}".format(contact_username, username))
    response['status'] = 'ok'
    return response

# 添加联系人
def lib_delete_contact(username, contact_username):
    hash_key = 'contact:' + username
    response = {}

    try:
        redis_client = redis.StrictRedis.from_url(config['REDIS_REMOTE_URL'])
        redis_client.hdel(hash_key, contact_username)
    except:
        logger.error("ERROR! Cannot connect to {}".format(config['REDIS_REMOTE_URL']))
        response['status'] = 'err'
        response['data'] = "连接数据库错误!"
        return response

    logger.debug("Success delete contact contact:{} {}".format(contact_username, username))
    response['status'] = 'ok'
    return response

# 列出联系人列表
def lib_get_contact(username):
    hash_key = 'contact:' + username
    response = {}

    try:
        redis_client = redis.StrictRedis.from_url(config['REDIS_LOCAL_URL'])
        redis_data = redis_client.hvals(hash_key)
    except:
        logger.error("ERROR! Cannot connect to {}".format(config['REDIS_LOCAL_URL']))
        response['status'] = 'err'
        response['data'] = "连接数据库错误!"
        return response

    response['status'] = 'ok'
    response['data'] = [ json.loads(el.decode('utf-8')) for el in redis_data ]
    return response