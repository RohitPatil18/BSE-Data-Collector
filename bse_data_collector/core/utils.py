import redis
from bse_data_collector.settings import REDIS_DATABASE


def connect_db():
    # pool = redis.ConnectionPool(
    #     host=REDIS_DATABASE['HOST'],
    #     port=REDIS_DATABASE['PORT'],
    #     db=REDIS_DATABASE['DB']
    # )
    r = redis.StrictRedis(
        host=REDIS_DATABASE['HOST'],
        port=REDIS_DATABASE['PORT'],
        db=REDIS_DATABASE['DB'],
        decode_responses=True
    )
    return r