from fastapi import APIRouter, Request, status
from typing import Optional

from src.common.models import UserDto, Role, TokenDto
from src.common.telegram_valdiator import TelegramInitData

from src.api.src.builders.response_builder import ResponseBuilder
from src.api.src.database.crud.user_crud import UserCRUD
from src.api.src.database.db_setup import DbContext
from src.api.src.routers.api_enpoints import APIEndpoints
from src.api.src.utils.string_utils import StringUtils
from src.api.src.utils.token_utils import TokenUtils


router = APIRouter()


@router.get(path=APIEndpoints.Authentication.Me, status_code=status.HTTP_200_OK, response_model=TokenDto,
            summary="Validates telegram user and returns token")
async def validate_telegram_user(request: Request, db: DbContext):
    init_data: Optional[str] = request.headers.get("Init-Data")

    if not init_data:
        return ResponseBuilder.error_response(message='Telegram Init-Data is missing')

    if not TelegramInitData.validate(init_data):
        return ResponseBuilder.error_response(message='Telegram Init-Data validation failed')

    user_id = StringUtils.get_prop_as_int(init_data, "user", "id")

    db_user = UserCRUD.get_user(user_id, db)

    if db_user is None:
        return ResponseBuilder.error_response(message='User was not found')

    user = UserDto.model_validate(db_user)

    payload = {
        "id": user.id,
        "first_name": user.first_name,
        "last_name": user.last_name
    }

    if user.is_admin:
        payload["role"] = Role.Admin
    else:
        payload["role"] = Role.Tutor if user.is_tutor else Role.Student

    token = TokenUtils.create_access_token(payload)

    result = TokenDto(token=token)

    return ResponseBuilder.success_response(content=result)


@router.get(path=APIEndpoints.Authentication.Tg, status_code=status.HTTP_200_OK, response_model=TokenDto,
            summary="Validates telegram user and returns token for bot")
async def validate_telegram_user(request: Request, db: DbContext):
    init_data: Optional[str] = request.headers.get("Init-Data")

    if not init_data:
        return ResponseBuilder.error_response(message='Telegram Init-Data is missing')

    if not TelegramInitData.validate(init_data):
        return ResponseBuilder.error_response(message='Telegram Init-Data validation failed')

    user_id = StringUtils.get_prop_as_int(init_data, "user", "id")

    db_user = UserCRUD.get_user(user_id, db)

    payload = dict()

    if db_user is None:
        payload.update({
            "id": user_id,
            "registered": False,
            "first_name": StringUtils.get_prop_as_int(init_data, "user", "first_name"),
            "last_name": StringUtils.get_prop_as_int(init_data, "user", "last_name")
        })
    else:
        user = UserDto.model_validate(db_user)

        payload = {
            "id": user.id,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "registered": True
        }

        if user.is_admin:
            payload["role"] = Role.Admin
        elif user.is_student or user.is_tutor:
            payload["role"] = Role.Tutor if user.is_tutor else Role.Student

    token = TokenUtils.create_access_token(payload)

    result = TokenDto(token=token)

    return ResponseBuilder.success_response(content=result)
