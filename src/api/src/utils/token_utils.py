import hashlib
import jwt
from datetime import datetime, timedelta, timezone
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from typing import Annotated, Optional

from src.common.config import access_token_expire_minutes, bot_token, algorithm
from src.common.models import BaseDto, Role


class UserContextModel(BaseDto):
    id: int
    first_name: str
    last_name: str
    role: Optional[Role] = None
    exp: int
    registered: Optional[bool] = False

    class Config:
        from_attributes = True


class TokenUtils:
    oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

    @classmethod
    def create_access_token(cls, data: dict):
        to_encode = data.copy()

        expires_delta = timedelta(minutes=access_token_expire_minutes)
        expire = datetime.now(timezone.utc) + expires_delta

        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, cls.__get_secret_key(), algorithm=algorithm)

        return encoded_jwt

    @classmethod
    async def get_current_user(cls, token: Annotated[str, Depends(oauth2_scheme)]) -> UserContextModel:
        payload = TokenUtils.decode_token(token)

        user = UserContextModel.model_validate(payload)

        return user

    @classmethod
    def decode_token(cls, token: str) -> dict:
        try:
            decoded_token = jwt.decode(token, cls.__get_secret_key(), algorithms=[algorithm, ])

            return decoded_token
        except jwt.ExpiredSignatureError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token has expired.",
                headers={"WWW-Authenticate": "Bearer"}
            )
        except jwt.InvalidTokenError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token.",
                headers={"WWW-Authenticate": "Bearer"}
            )

    @classmethod
    def __get_secret_key(cls) -> bytes:
        return hashlib.sha256(bot_token.encode()).digest()


async def get_current_active_user(current_user: Annotated[UserContextModel, Depends(TokenUtils.get_current_user)]) -> UserContextModel:
    return current_user


UserContext = Annotated[UserContextModel, Depends(get_current_active_user)]
