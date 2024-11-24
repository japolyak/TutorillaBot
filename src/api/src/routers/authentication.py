from fastapi import APIRouter, Request, status

from src.common.models import TokenDto
from src.common.telegram_init_data import TelegramInitData

from src.api.src.builders.response_builder import ResponseBuilder
from src.api.src.database.crud.user_crud import UserCRUD
from src.api.src.database.db_setup import DbContext
from src.api.src.routers.api_enpoints import APIEndpoints
from src.api.src.utils.token_utils import TokenUtils, RefreshUserContext, TokenPayload


router = APIRouter()


@router.get(path=APIEndpoints.Authentication.Me, status_code=status.HTTP_200_OK, response_model=TokenDto,
            summary="Validates telegram user from bot and returns token for bot")
async def validate_bot_user(request: Request, db: DbContext):
    init_data = TelegramInitData(request.headers.get("Init-Data"))

    if not init_data.user:
        return ResponseBuilder.error_response(message='Telegram Init-Data is missing')

    if not init_data.is_valid():
        return ResponseBuilder.error_response(message='Telegram Init-Data validation failed')

    db_user = UserCRUD.get_user(init_data.user.id, db)

    if db_user is None:
        if init_data.from_bot:
            payload = TokenPayload.initial_user(init_data.user)
        else:
            return ResponseBuilder.error_response(message='User was not found')
    else:
        payload = TokenPayload.from_db_model(db_user)

    access_token, session_key = TokenUtils.create_token_pair(payload)

    result = TokenDto(access_token=access_token)

    return ResponseBuilder.success_response(content=result, cookies={ 'sessionKey': session_key })


@router.get(path=APIEndpoints.Authentication.Prolong, status_code=status.HTTP_200_OK, response_model=TokenDto,
            summary="Refreshes access token")
async def refresh_access_token(user: RefreshUserContext, db: DbContext):
    if user.registered:
        db_user = UserCRUD.get_user(user.id, db)

        if db_user is None:
            return ResponseBuilder.error_response(message='User was not found')
        payload = TokenPayload.from_db_model(db_user)
    else:
        payload = TokenPayload.from_user_context(user)

    access_token, session_key = TokenUtils.create_token_pair(payload)

    result = TokenDto(access_token=access_token)

    return ResponseBuilder.success_response(content=result, cookies={ 'sessionKey': session_key })