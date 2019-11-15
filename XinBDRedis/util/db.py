import redis
from util.default_settings import redis_settings


def get_redis_cli():
    return redis.StrictRedis(**redis_settings)
