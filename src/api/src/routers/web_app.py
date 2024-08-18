from fastapi import APIRouter, Request, status, Depends
from sqlalchemy.orm import Session

from src.common.models import UserDto

from src.api.src.builders.response_builder import ResponseBuilder
from src.api.src.database.crud import user_crud
from src.api.src.database.db_setup import session
from src.api.src.functions.telegram_valdiator import init_data_is_valid
from src.api.src.routers.api_enpoints import APIEndpoints
from src.api.src.utils.string_utils import StringUtils


router = APIRouter()


@router.get(path=APIEndpoints.WebApp.Me, status_code=status.HTTP_200_OK, response_model=UserDto,
            summary="Validates telegram user and returns user data")
async def validate_telegram_user(request: Request, db: Session = Depends(session)):
    init_data: None or str = request.headers.get("Init-Data")

    if not init_data:
        return ResponseBuilder.error_response(message='Telegram Init-Data is missing')

    if not init_data_is_valid(init_data):
        return ResponseBuilder.error_response(message='Telegram Init-Data validation failed')

    user_id = StringUtils.get_prop_as_int(init_data, "user", "id")

    db_user = user_crud.get_user(db=db, user_id=user_id)

    if db_user is None:
        return ResponseBuilder.error_response(message='User was not found')

    db_user = UserDto.model_validate(db_user)

    return ResponseBuilder.success_response(content=db_user)
