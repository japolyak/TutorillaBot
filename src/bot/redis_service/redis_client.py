import redis
from src.bot.config import redis_host, redis_db, redis_password, redis_username

r = redis.Redis(
    host=redis_host,
    db=redis_db,
    password=redis_password,
    username=redis_username,
    decode_responses=True
)
