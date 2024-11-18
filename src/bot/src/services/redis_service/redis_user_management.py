from redis import Redis
from typing import Literal

from src.common.models import UserDto, Role
from src.bot.src.redis_configuration import redis_instance


class RedisManagement:
    __r: Redis = redis_instance

    def add_user(self, user_id: str, user: UserDto):
        self.__r.hset(user_id, "id", int(user.id))
        self.__r.hset(user_id, "first_name", user.first_name)
        self.__r.hset(user_id, "last_name", user.last_name)
        self.__r.hset(user_id, "email", user.email)
        self.__r.hset(user_id, "time_zone", user.time_zone)

        self.__r.hset(user_id, "locale", user.locale)
        self.__r.hset(user_id, "is_active", int(user.is_active))
        self.__r.hset(user_id, "is_student", int(user.is_student))
        self.__r.hset(user_id, "is_tutor", int(user.is_tutor))
        self.__r.hset(user_id, "is_admin", int(user.is_admin))

    def has_role(self, user_id: str, role: Literal[Role.Tutor, Role.Student, Role.Admin]):
        match role:
            case Role.Tutor:
                return self.__r.hget(user_id, "is_tutor") == "1"
            case Role.Student:
                return self.__r.hget(user_id, "is_student") == "1"
            case Role.Admin:
                return self.__r.hget(user_id, "is_admin") == "1"
            case _:
                return False

    def get_user_token(self, user_id: int):
        user_id = str(user_id)

        return self.__r.hget(user_id, "Bearer")

    def set_user_token(self, user_id: int, token: str):
        user_id = str(user_id)

        return self.__r.hset(user_id, "Bearer", token)
