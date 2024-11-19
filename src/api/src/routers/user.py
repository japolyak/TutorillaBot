from fastapi import status, APIRouter
from typing import Literal

from src.common.models import UserDto, UserBaseDto, Role

from src.api.src.builders.response_builder import ResponseBuilder
from src.api.src.database.crud.user_crud import UserCRUD
from src.api.src.database.crud.user_requests_crud import UserRequestCRUD
from src.api.src.database.db_setup import DbContext
from src.api.src.routers.api_enpoints import APIEndpoints
from src.api.src.utils.token_utils import UserContext


router = APIRouter()


@router.get(
    path=APIEndpoints.Users.Me,
    status_code=status.HTTP_200_OK,
    response_model=UserDto,
    summary="Gets user"
)
async def get_me(user_context: UserContext, db: DbContext):
    db_user = UserCRUD.get_user(user_context.id, db)

    if db_user is None:
        return ResponseBuilder.error_response(message='User was not found')

    user = UserDto.model_validate(db_user)

    return ResponseBuilder.success_response(content=user)


@router.post(path=APIEndpoints.Users.Post, status_code=status.HTTP_201_CREATED, summary="Adds a new user")
async def register_user(user: UserBaseDto, user_context: UserContext, db: DbContext):
    if user_context.registered or user_context.role in [Role.Student, Role.Tutor]:
        return ResponseBuilder.error_response(message='User was already registered')

    user_created = UserCRUD.create_user(user, db)

    if not user_created:
        return ResponseBuilder.error_response(message='User was not created')

    return ResponseBuilder.success_response(status.HTTP_201_CREATED)


@router.post(path=APIEndpoints.Users.ApplyRole, status_code=status.HTTP_201_CREATED,
             summary="Applies user's request for a role")
async def apply_for_role(role: Literal[Role.Student, Role.Tutor], user_context: UserContext, db: DbContext):
    if not user_context.registered:
        return ResponseBuilder.error_response(message='User is not registered')

    if user_context.role in [Role.Student, Role.Tutor]:
        return ResponseBuilder.error_response(message='User already has roles')

    request_created = UserRequestCRUD.create_user_request(user_context.id, role, db)

    if not request_created:
        return ResponseBuilder.error_response(message='Role application was not successful')

    return ResponseBuilder.success_response(status.HTTP_201_CREATED)
