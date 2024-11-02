from fastapi import status, APIRouter
from typing import Literal

from src.common.models import UserDto, UserRequestDto, Role, ItemsDto, StatisticsDto

from src.api.src.bot_client.message_sender import send_decline_message
from src.api.src.builders.response_builder import ResponseBuilder
from src.api.src.database.crud.user_crud import UserCRUD
from src.api.src.database.crud.admin_crud import AdminCRUD
from src.api.src.database.db_setup import DbContext
from src.api.src.routers.api_enpoints import APIEndpoints


router = APIRouter()


@router.get(path=APIEndpoints.Admin.RequestsStatistics, status_code=status.HTTP_200_OK,
            response_model=StatisticsDto, summary="Get requests statistics")
async def get_requests_statistics(db: DbContext):
    students, tutors = AdminCRUD.requests_statistics(db)

    response_model = StatisticsDto(students_requests=students, tutors_requests=tutors)

    return ResponseBuilder.success_response(content=response_model)


@router.get(path=APIEndpoints.Admin.GetRequests, status_code=status.HTTP_200_OK,
            response_model=ItemsDto[UserRequestDto], summary="Get all requests by role")
async def get_requests(role: Literal[Role.Student, Role.Tutor], db: DbContext):
    requests = AdminCRUD.get_users_requests(db=db, role=role)

    if not requests:
        return ResponseBuilder.success_response(content=ItemsDto(items=[]))

    mapped_requests = [UserRequestDto(id=r[0],
                                      user_id=r[1],
                                      user_first_name=r[2],
                                      user_last_name=r[3],
                                      user_email=r[4],
                                      user_role=r[5]
                                      ) for r in requests]

    return ResponseBuilder.success_response(content=ItemsDto[UserRequestDto](items=mapped_requests))


@router.get(path=APIEndpoints.Admin.GetRequest, status_code=status.HTTP_200_OK, response_model=UserRequestDto,
            summary="Get request by request id")
async def get_request(role_request_id: int, db: DbContext):
    db_request = AdminCRUD.get_user_request(db, role_request_id)

    if db_request is None:
        return ResponseBuilder.error_response(message='User request was not found')

    response_model = UserRequestDto(id=db_request[0],
                                    user_id=db_request[1],
                                    user_first_name=db_request[2],
                                    user_last_name=db_request[3],
                                    user_email=db_request[4],
                                    user_role=db_request[5])

    return ResponseBuilder.success_response(content=response_model)


@router.put(path=APIEndpoints.Admin.AcceptRole, status_code=status.HTTP_200_OK, response_model=UserDto,
            summary="Accept user role request")
async def accept_role(user_id: int, role: Literal[Role.Student], db: DbContext):
    # TODO - rewrite
    db_user = UserCRUD.get_user(db=db, user_id=user_id)

    if db_user is None:
        return ResponseBuilder.error_response(message='User was not found')

    if db_user.is_tutor:
        return ResponseBuilder.error_response(message='User has tutor role')

    if db_user.is_student:
        return ResponseBuilder.error_response(message='User has student role')

    response_model = UserCRUD.accept_role_request(db=db, user_id=user_id, role=role)

    if not response_model:
        return ResponseBuilder.error_response(message='Role request was not found')

    return ResponseBuilder.success_response(content=response_model)


@router.put(path=APIEndpoints.Admin.DeclineRole, status_code=status.HTTP_200_OK, summary="Decline user role request")
async def decline_student_role(user_id: int, db: DbContext):
    # TODO - rewrite
    db_user = UserCRUD.get_user(db=db, user_id=user_id)

    if db_user is None:
        return ResponseBuilder.error_response(message='User was not found')

    declination = UserCRUD.decline_role_request(db=db, user_id=user_id)

    if not declination:
        return ResponseBuilder.error_response(message='Role request was not found')

    send_decline_message(db_user.id)

    return ResponseBuilder.success_response()
