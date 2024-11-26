from fastapi import Depends
from typing import Annotated

from src.api.src.utils.token_utils import TokenUtils, UserContextModel


async def get_current_user(current_user: Annotated[UserContextModel, Depends(TokenUtils.get_current_user)]) -> UserContextModel:
    return current_user


UserContext = Annotated[UserContextModel, Depends(get_current_user)]
