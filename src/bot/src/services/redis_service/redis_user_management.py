from redis import Redis

from src.common.models import UserDto


class RedisUser:
    @staticmethod
    def add_user(redis: Redis, user_id: int, user: UserDto):
        redis.hset(user_id, "id", int(user.id))
        redis.hset(user_id, "first_name", user.first_name)
        redis.hset(user_id, "last_name", user.last_name)
        redis.hset(user_id, "email", user.email)
        redis.hset(user_id, "time_zone", user.time_zone)

        redis.hset(user_id, "locale", user.locale)
        redis.hset(user_id, "is_active", int(user.is_active))
        redis.hset(user_id, "is_student", int(user.is_student))
        redis.hset(user_id, "is_tutor", int(user.is_tutor))
        redis.hset(user_id, "is_admin", int(user.is_admin))
