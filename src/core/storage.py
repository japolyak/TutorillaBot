from redis import Redis
from typing import Literal, Optional
from datetime import timedelta

from src.core.config import access_token_ttl_in_minutes, refresh_token_ttl_in_days
from src.core.models import UserDto, Role
from src.core.redis_configuration import redis_instance


class Storage:
    __r: Redis = redis_instance
    access_token_key = "accessToken"
    refresh_token_key = "refreshToken"
    refresh_token_id_key = "refreshTokenId"

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

    def get_access_token(self, user_id: int) -> Optional[str]:
        return self.__r.getex(f"{self.access_token_key}:{user_id}")

    def set_access_token(self, user_id: int, access_token: str):
        access_token_ttl = timedelta(minutes=access_token_ttl_in_minutes)
        self.__r.setex(f"{self.access_token_key}:{user_id}", access_token_ttl, access_token)

    def get_refresh_token_id(self, user_id: int) -> Optional[str]:
        return self.__r.getex(f"{self.refresh_token_id_key}:{user_id}")

    def set_refresh_token_id(self, user_id: int, refresh_token_id: str):
        refresh_token_ttl = timedelta(days=refresh_token_ttl_in_days)
        self.__r.setex(f"{self.refresh_token_id_key}:{user_id}", refresh_token_ttl, refresh_token_id)

    def set_refresh_token(self, refresh_token_id: str, token: str):
        refresh_token_ttl = timedelta(days=refresh_token_ttl_in_days)

        self.__r.setex(f"{self.refresh_token_key}:{refresh_token_id}", refresh_token_ttl, token)

    def get_refresh_token(self, refresh_token_id: str) -> Optional[str]:
        return self.__r.getex(f"{self.refresh_token_key}:{refresh_token_id}")

    def delete_session(self, user_id: int):
        names = [f"{self.access_token_key}:{user_id}", f"{self.refresh_token_id_key}:{user_id}"]
        refresh_token_id = self.get_refresh_token_id(user_id)

        if refresh_token_id:
            names.append(f"{self.refresh_token_key}:{refresh_token_id}")

        self.__r.delete(*names)
