from hashlib import sha256
from time import time
from jwt import encode, decode, ExpiredSignatureError, InvalidTokenError
from datetime import datetime, timedelta, timezone
from fastapi import Depends, HTTPException, status, Cookie
from fastapi.security import OAuth2PasswordBearer
from typing import Annotated, Optional, Tuple

from src.common.config import bot_token, algorithm, access_token_ttl_in_minutes, refresh_token_ttl_in_days
from src.common.models import BaseDto, Role
from src.common.storage import Storage
from src.common.telegram_init_data import TelegramUser

from src.api.src.database.models import User


class RefreshUserContextModel(BaseDto):
    id: int
    first_name: str
    last_name: str
    registered: Optional[bool] = False


class UserContextModel(BaseDto):
    id: int
    first_name: str
    last_name: str
    role: Optional[Role] = None
    exp: int
    registered: Optional[bool] = False


class TokenPayload(BaseDto):
    id: int
    first_name: str
    last_name: str
    role: Optional[Role] = None
    registered: Optional[bool] = False

    @classmethod
    def from_db_model(cls, user: User):
        if user.is_admin:
            role = Role.Admin
        else:
            role = Role.Tutor if user.is_tutor else Role.Student

        return cls(id=user.id, first_name=user.first_name, last_name=user.last_name, role=role, registered=True)

    @classmethod
    def from_user_context(cls, user: RefreshUserContextModel):
        return cls(id=user.id, first_name=user.first_name, last_name=user.last_name)

    @classmethod
    def initial_user(cls, user: TelegramUser):
        return cls(id=user.id, first_name=user.first_name, last_name=user.last_name)


class TokenUtils:
    oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

    @classmethod
    def create_token_pair(cls, payload: TokenPayload) -> Tuple[str, str]:
        access_token = cls.__create_token(payload.model_dump(), minutes=access_token_ttl_in_minutes)
        refresh_token = cls.__create_token(payload.model_dump(exclude={"role"}), days=refresh_token_ttl_in_days)
        session_key = cls.__create_refresh_key(payload.id)

        Storage().set_user_refresh_token(session_key, refresh_token)

        return access_token, session_key

    @classmethod
    def __create_token(cls, data: dict, days=0, minutes=0):
        to_encode = data.copy()

        token_ttl = timedelta(days=days, minutes=minutes)
        expires = datetime.now(timezone.utc) + token_ttl

        to_encode.update({"exp": expires})
        encoded_jwt = encode(to_encode, cls.__get_secret_key(), algorithm=algorithm)

        return encoded_jwt

    @classmethod
    def __create_refresh_key(cls, user_id: int) -> str:
        timestamp = time()
        raw_data = f"{user_id}:{timestamp}"

        session_key = sha256(raw_data.encode()).hexdigest()
        return session_key

    @classmethod
    async def get_current_user(cls, token: Annotated[str, Depends(oauth2_scheme)]) -> UserContextModel:
        payload = TokenUtils.decode_token(token)

        user = UserContextModel.model_validate(payload)

        return user

    @classmethod
    async def get_refresh_user(
            cls,
            session_key: Annotated[str | None, Cookie(alias="sessionKey")] = None
    ) -> RefreshUserContextModel:
        refresh_token = Storage().get_refresh_token(session_key)

        if not refresh_token:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Session has expired."
            )

        payload = TokenUtils.decode_token(refresh_token)

        user = RefreshUserContextModel.model_validate(payload)

        return user

    @classmethod
    def decode_token(cls, token: str) -> dict:
        try:
            decoded_token = decode(token, cls.__get_secret_key(), algorithms=[algorithm, ])

            return decoded_token
        except ExpiredSignatureError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token has expired.",
                headers={"WWW-Authenticate": "Bearer"}
            )
        except InvalidTokenError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token.",
                headers={"WWW-Authenticate": "Bearer"}
            )

    @classmethod
    def __get_secret_key(cls) -> bytes:
        return sha256(bot_token.encode()).digest()
