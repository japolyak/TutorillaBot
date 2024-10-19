from redis import Redis
from telebot.storage import StateRedisStorage

from common import redis_host, redis_db, redis_password, redis_username

redis_instance = Redis(
    host=redis_host,
    db=redis_db,
    password=redis_password,
    username=redis_username,
    decode_responses=True
)

state_storage = StateRedisStorage(
    host=redis_host,
    db=redis_db,
    password=redis_password
)
