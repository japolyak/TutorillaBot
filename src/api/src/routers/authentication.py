from fastapi import APIRouter, Request, status
from urllib.parse import parse_qs

from src.common.models import UserDto, Role, TokenDto

from src.api.src.builders.response_builder import ResponseBuilder
from src.api.src.database.crud import user_crud
from src.api.src.database.db_setup import DbContext
from src.api.src.functions.telegram_valdiator import init_data_is_valid
from src.api.src.routers.api_enpoints import APIEndpoints
from src.api.src.utils.string_utils import StringUtils
from src.api.src.utils.token_utils import TokenUtils


router = APIRouter()


@router.get(path=APIEndpoints.Authentication.Me, status_code=status.HTTP_200_OK, response_model=UserDto,
            summary="Validates telegram user and returns user data")
async def validate_telegram_user(request: Request, db: DbContext):
    init_data: None or str = request.headers.get("Init-Data")

    if not init_data:
        return ResponseBuilder.error_response(message='Telegram Init-Data is missing')

    parsed_init_data = parse_qs(init_data)

    if not init_data_is_valid(parsed_init_data):
        return ResponseBuilder.error_response(message='Telegram Init-Data validation failed')

    user_id = StringUtils.get_prop_as_int(init_data, "user", "id")

    db_user = user_crud.get_user(db=db, user_id=user_id)

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
    user.normalized_email = token
    result = TokenDto(token=token)

    return ResponseBuilder.success_response(content=result)
