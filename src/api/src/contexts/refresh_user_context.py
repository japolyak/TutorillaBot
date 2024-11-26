from fastapi import Depends
from typing import Annotated

from src.api.src.utils.token_utils import TokenUtils, RefreshUserContextModel


async def get_refresh_user(current_user: Annotated[RefreshUserContextModel, Depends(TokenUtils.get_refresh_user)]) -> RefreshUserContextModel:
    return current_user


RefreshUserContext = Annotated[RefreshUserContextModel, Depends(get_refresh_user)]
