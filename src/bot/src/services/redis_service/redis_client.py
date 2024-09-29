from redis import Redis

from common import redis_host, redis_db, redis_password, redis_username

r = Redis(
    host=redis_host,
    db=redis_db,
    password=redis_password,
    username=redis_username,
    decode_responses=True
)
