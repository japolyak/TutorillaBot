from redis import Redis

from src.core.config import redis_host, redis_db, redis_username

redis_instance = Redis(
    host=redis_host,
    db=redis_db,
    username=redis_username,
    decode_responses=True
)