import jwt
import hashlib
from datetime import datetime, timedelta, timezone

from src.common.config import access_token_expire_minutes, bot_token, algorithm

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
        print(header_data)

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