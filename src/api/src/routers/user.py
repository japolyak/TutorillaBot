from fastapi import status, APIRouter
from typing import Literal

from src.common.models import UserDto, UserBaseDto, Role

from src.api.src.builders.response_builder import ResponseBuilder
from src.api.src.database.crud.user_crud import UserCRUD
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
    db_user = UserCRUD.get_user(db=db, user_id=user_context.id)

    if db_user is None:
        return ResponseBuilder.error_response(message='User was not found')

    user = UserDto.model_validate(db_user)

    return ResponseBuilder.success_response(content=user)


@router.get(
    path=APIEndpoints.Users.GetUser,
    status_code=status.HTTP_200_OK,
    response_model=UserDto,
    summary="Gets user by id"
)
async def get_user(user_id: int, db: DbContext):
    db_user = UserCRUD.get_user(db=db, user_id=user_id)

    if db_user is None:
        return ResponseBuilder.error_response(message='User was not found')

    return ResponseBuilder.success_response(content=db_user)


@router.post(path=APIEndpoints.Users.Post, status_code=status.HTTP_201_CREATED, summary="Adds a new user")
async def register_user(user: UserBaseDto, db: DbContext):
    return ResponseBuilder.success_response(status.HTTP_201_CREATED)
    # TODO - refactor
    result = db.execute(sql_statements.add_user, params)

    error_msg = result.fetchall()[0][0]

    db.commit()
    db.close()

    return ResponseBuilder.success_response(status.HTTP_201_CREATED)\
        if not error_msg\
        else ResponseBuilder.error_response(message='User addition was not successful')


@router.post(path=APIEndpoints.Users.ApplyRole, status_code=status.HTTP_201_CREATED,
             summary="Applies user's request for a role")
async def apply_for_role(user_id: int, role: Literal[Role.Student, Role.Tutor], db: DbContext):
    return ResponseBuilder.success_response(status.HTTP_201_CREATED)
    # TODO - refactor
    result = db.execute(sql_statements.add_user_role_request, params)

    error_msg = result.fetchall()[0][0]

    db.commit()
    db.close()

    if error_msg is not None:
        return ResponseBuilder.error_response(message='Role application was not successful')

    return ResponseBuilder.success_response(status.HTTP_201_CREATED)
