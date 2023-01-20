import redis
from config import REDIS_DB_URL


def connect_redis():
    return redis.Redis(**REDIS_DB_URL)


def get_redis_data(key):
    conn = connect_redis()
    data = conn.get(key)
    return data


def set_redis_data(key, value):
    conn = connect_redis()
    data = value
    conn.set(
        name=key,
        value=data,
        #ex=""  # 第三个参数表示Redis过期时间,不设置则默认不过期
    )
    # 存到Redis


def check_key(key):
    conn = connect_redis()
    data = conn.exists(key)
    if data == 1:
        return True
    else:
        return False


def del_key(key):
    conn = connect_redis()
    data = conn.delete(key)
    if data == 1:
        return True
    else:
        return False
