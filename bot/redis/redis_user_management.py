from bot.redis.redis_client import r
from ..api.api_models import UserDto


def add_user(user_id: int, user: UserDto):
    r.hset(user_id, "id", int(user.id))
    r.hset(user_id, "first_name", user.first_name)
    r.hset(user_id, "last_name", user.last_name)
    r.hset(user_id, "email", user.email)
    r.hset(user_id, "phone_number", user.phone_number)
    r.hset(user_id, "time_zone", user.time_zone)

    r.hset(user_id, "locale", user.locale)
    r.hset(user_id, "is_student", int(user.is_student))
    r.hset(user_id, "is_tutor", int(user.is_tutor))
    r.hset(user_id, "is_admin", int(user.is_admin))