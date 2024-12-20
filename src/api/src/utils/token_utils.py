from hashlib import sha256
from time import time
from jwt import encode, decode, ExpiredSignatureError, InvalidTokenError
from datetime import datetime, timedelta, timezone
from fastapi import Depends, HTTPException, status, Cookie
from fastapi.security import OAuth2PasswordBearer
from typing import Annotated, Optional, Tuple, Literal, List

from src.core.config import bot_token, algorithm, access_token_ttl_in_minutes, refresh_token_ttl_in_days
from src.core.models import BaseDto, Role, Scope
from src.core.storage import Storage
from src.core.logger import log
from src.core.telegram_init_data import TelegramUser

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
    roles: List[Role] = []
    exp: int
    registered: Optional[bool] = False

    def has_any_role(self, roles: Tuple[Role]) -> bool:
        return any(role in self.roles for role in roles)

    def has_role(self, role: Role) -> bool:
        return role in self.roles


class TokenPayload(BaseDto):
    id: int
    first_name: str
    last_name: str
    roles: List[Role] = []
    registered: Optional[bool] = False

    @classmethod
    def from_db_model(cls, user: User):
        roles: List[Role] = []

        if user.is_admin: roles.append(Role.Admin)
        if user.is_student: roles.append(Role.Student)
        if user.is_tutor: roles.append(Role.Tutor)

        return cls(id=user.id, first_name=user.first_name, last_name=user.last_name, registered=True, roles=roles)

    @classmethod
    def from_user_context(cls, user: RefreshUserContextModel):
        return cls(id=user.id, first_name=user.first_name, last_name=user.last_name)

    @classmethod
    def initial_user(cls, user: TelegramUser):
        return cls(id=user.id, first_name=user.first_name, last_name=user.last_name)


class TokenUtils:
    oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

    @classmethod
    def create_token_pair(cls, payload: TokenPayload, scope: Literal[Scope.Bot, Scope.WebApp]) -> Tuple[str, str]:
        refresh_token_id = Storage().get_refresh_token_id(payload.id)

        if not refresh_token_id:
            refresh_token = cls._create_token(payload.model_dump(exclude={"role"}), days=refresh_token_ttl_in_days)
            refresh_token_id = cls._create_refresh_key(payload.id)
            Storage().set_refresh_token(refresh_token_id, refresh_token)

            if scope == Scope.WebApp:
                Storage().set_refresh_token_id(payload.id, refresh_token_id)

        access_token = cls.create_access_token(payload)

        return access_token, refresh_token_id

    @classmethod
    def create_access_token(cls, payload: TokenPayload) -> str:
        return cls._create_token(payload.model_dump(), minutes=access_token_ttl_in_minutes)

    @classmethod
    async def get_current_user(cls, token: Annotated[str, Depends(oauth2_scheme)]) -> UserContextModel:
        payload = TokenUtils._decode_token(token)

        user = UserContextModel.model_validate(payload)

        return user

    @classmethod
    async def get_refresh_user(
            cls,
            session_key: Annotated[str | None, Cookie(alias="refreshTokenId")] = None
    ) -> RefreshUserContextModel:
        refresh_token = Storage().get_refresh_token(session_key)

        if not refresh_token:
            message = "Session has expired"

            log.exception(msg=message)
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=message)

        payload = TokenUtils._decode_token(refresh_token)

        user = RefreshUserContextModel.model_validate(payload)

        return user

    #region Private methods
    @classmethod
    def _create_token(cls, data: dict, days=0, minutes=0):
        to_encode = data.copy()

        token_ttl = timedelta(days=days, minutes=minutes)
        expires = datetime.now(timezone.utc) + token_ttl

        to_encode.update({"exp": expires})
        encoded_jwt = encode(to_encode, cls._get_secret_key(), algorithm=algorithm)

        return encoded_jwt

    @classmethod
    def _create_refresh_key(cls, user_id: int) -> str:
        timestamp = time()
        raw_data = f"{user_id}:{timestamp}"

        session_key = sha256(raw_data.encode()).hexdigest()
        return session_key

    @classmethod
    def _get_secret_key(cls) -> bytes:
        return sha256(bot_token.encode()).digest()

    @classmethod
    def _decode_token(cls, token: str) -> dict:
        try:
            decoded_token = decode(token, cls._get_secret_key(), algorithms=[algorithm, ])

            return decoded_token
        except ExpiredSignatureError:
            message = "Token has expired"

            log.exception(msg=message)
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=message,
                headers={"WWW-Authenticate": "Bearer"}
            )
        except InvalidTokenError:
            message = "Invalid token"

            log.exception(msg=message)
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=message,
                headers={"WWW-Authenticate": "Bearer"}
            )
    #endregion