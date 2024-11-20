from fastapi import APIRouter, Request, status
from typing import Optional

from src.common.models import TokenDto
from src.common.telegram_valdiator import TelegramInitData

from src.api.src.builders.response_builder import ResponseBuilder
from src.api.src.database.crud.user_crud import UserCRUD
from src.api.src.database.db_setup import DbContext
from src.api.src.routers.api_enpoints import APIEndpoints
from src.api.src.utils.string_utils import StringUtils
from src.api.src.utils.token_utils import TokenUtils, RefreshUserContext, TokenPayload


router = APIRouter()


def get_and_validate_init_data(init_data: Optional[str]):
    if not init_data:
        return ResponseBuilder.error_response(message='Telegram Init-Data is missing')

    if not TelegramInitData.validate(init_data):
        return ResponseBuilder.error_response(message='Telegram Init-Data validation failed')


@router.get(path=APIEndpoints.Authentication.Me, status_code=status.HTTP_200_OK, response_model=TokenDto,
            summary="Validates telegram user from web-app and returns token")
async def validate_web_app_user(request: Request, db: DbContext):
    init_data: Optional[str] = request.headers.get("Init-Data")

    init_data_validation_result =  get_and_validate_init_data(init_data)

    if init_data_validation_result is not None:
        return init_data_validation_result

    user_id = StringUtils.get_prop_as_int(init_data, "user", "id")

    db_user = UserCRUD.get_user(user_id, db)

    if db_user is None:
        return ResponseBuilder.error_response(message='User was not found')

    payload = TokenPayload.from_db_model(db_user)

    access_token, refresh_token = TokenUtils.create_token_pair(payload)

    result = TokenDto(access_token=access_token, refresh_token=refresh_token)

    return ResponseBuilder.success_response(content=result)


@router.get(path=APIEndpoints.Authentication.Tg, status_code=status.HTTP_200_OK, response_model=TokenDto,
            summary="Validates telegram user from bot and returns token for bot")
async def validate_bot_user(request: Request, db: DbContext):
    init_data: Optional[str] = request.headers.get("Init-Data")

    init_data_validation_result = get_and_validate_init_data(init_data)

    if init_data_validation_result is not None:
        return init_data_validation_result

    user_id = StringUtils.get_prop_as_int(init_data, "user", "id")

    db_user = UserCRUD.get_user(user_id, db)

    if db_user is None:
        payload_new = TokenPayload.initial_user(user_id, init_data)
    else:
        payload_new = TokenPayload.from_db_model(db_user)

    access_token, refresh_token = TokenUtils.create_token_pair(payload_new)

    result = TokenDto(access_token=access_token, refresh_token=refresh_token)

    return ResponseBuilder.success_response(content=result)


@router.get(path=APIEndpoints.Authentication.Prolong, status_code=status.HTTP_200_OK, response_model=TokenDto,
            summary="Prolongs access token")
async def prolong_access_token(user: RefreshUserContext, db: DbContext):
    if user.registered:
        db_user = UserCRUD.get_user(user.id, db)

        if db_user is None:
            return ResponseBuilder.error_response(message='User was not found')
        payload = TokenPayload.from_db_model(db_user)
    else:
        payload = TokenPayload.from_user_context(user)

    access_token, refresh_token = TokenUtils.create_token_pair(payload)

    result = TokenDto(access_token=access_token, refresh_token=refresh_token)

    return ResponseBuilder.success_response(content=result)
