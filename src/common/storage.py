from redis import Redis
from typing import Literal, Optional
from datetime import timedelta

from src.common.config import access_token_ttl_in_minutes, refresh_token_ttl_in_days
from src.common.models import UserDto, Role
from src.common.redis_configuration import redis_instance


class Storage:
    __r: Redis = redis_instance

    def add_user(self, user_id: int, user: UserDto):
        user_id = str(user_id)
        self.__r.hset(user_id, "id", user_id)
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

    def set_user_session(self, user_id: int, access_token: str, refresh_token: str):
        access_token_ttl = timedelta(minutes=access_token_ttl_in_minutes)
        refresh_token_ttl = timedelta(days=refresh_token_ttl_in_days)

        self.__r.setex(f"accessToken:{user_id}", access_token_ttl, access_token)
        self.__r.setex(f"sessionKey:{user_id}", refresh_token_ttl, refresh_token)

    def get_access_token(self, user_id: int) -> Optional[str]:
        return self.__r.getex(f"accessToken:{user_id}")

    def get_session_key(self, user_id: int) -> Optional[str]:
        return self.__r.getex(f"sessionKey:{user_id}")

    def set_user_refresh_token(self, key: str, token: str):
        refresh_token_ttl = timedelta(days=refresh_token_ttl_in_days)

        self.__r.setex(f"sessionKey:{key}", refresh_token_ttl, token)

    def get_refresh_token(self, session_key: str) -> Optional[str]:
        return self.__r.getex(f"sessionKey:{session_key}")

    def delete_session(self, user_id: int):
        names = [f"accessToken:{user_id}", f"sessionKey:{user_id}"]
        session_key = self.get_session_key(user_id)

        if session_key:
            names.append(f"sessionKey:{session_key}")

        self.__r.delete(*names)

    def delete_old_session(self, user_id: int, session_key: str):
        names = [f"sessionKey:{user_id}", f"sessionKey:{session_key}"]

        self.__r.delete(*names)
