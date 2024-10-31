import jwt
import hashlib
from typing import Annotated
from fastapi import Depends
from datetime import datetime, timedelta, timezone
from fastapi.security import OAuth2PasswordBearer

from src.common.config import access_token_expire_minutes, bot_token, algorithm
from src.common.models import BaseDto, Role


class UserContextModel(BaseDto):
    id: int
    first_name: str
    last_name: str
    role: Role
    exp: int

    class Config:
        from_attributes = True


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    try:
        payload = TokenUtils.decode_token(token)

        user = UserContextModel.model_validate(payload)

        return user
    except Exception as e:
        print(e)


async def get_current_active_user(current_user: Annotated[UserContextModel, Depends(get_current_user)]):
    return current_user


UserContext = Annotated[UserContextModel, Depends(get_current_active_user)]


class TokenUtils:

    @classmethod
    def create_access_token(cls, data: dict):
        to_encode = data.copy()

        expires_delta = timedelta(minutes=access_token_expire_minutes)
        expire = datetime.now(timezone.utc) + expires_delta

        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, cls.__get_secret_key(), algorithm=algorithm)

        return encoded_jwt

    @classmethod
    def decode_token(cls, token: str):
        header_data = jwt.get_unverified_header(token)

        return jwt.decode(token, cls.__get_secret_key(), algorithms=[algorithm, ])

    @classmethod
    def is_token_valid(cls, token: str) -> bool:
        return True

    @classmethod
    def is_token_expired(cls, token: str) -> bool:
        return True

    @classmethod
    def __get_secret_key(cls):
        return hashlib.sha256(bot_token.encode()).digest()