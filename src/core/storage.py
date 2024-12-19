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

    def add_user(self, user: UserDto):
        converted_user = {
            k: int(v) if isinstance(v, bool) else v for k, v in user.model_dump().items()
        }

        self.__r.hset(user.id, mapping=converted_user)

        return self

    def get_user(self, user_id: int) -> Optional[UserDto]:
        user = self.__r.hgetall(user_id)

        if not user: return None

        return UserDto.model_validate(user)

    def has_role(self, user_id: str, role: Literal[Role.Tutor, Role.Student, Role.Admin]):
        user = self.get_user(user_id)

        if not user: return False

        match role:
            case Role.Tutor:
                return user.is_tutor
            case Role.Student:
                return user.is_student
            case Role.Admin:
                return user.is_admin
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

        return self
