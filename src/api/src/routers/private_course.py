from fastapi import status, APIRouter
from typing import Literal

from src.core.models import Role, PrivateCourseInlineDto, ItemsDto, PrivateCourseDto, CourseMemberDto, ScheduleCourseDto

from src.api.src.builders.response_builder import ResponseBuilder
from src.api.src.contexts.db_contex import DbContext
from src.api.src.contexts.user_context import UserContext
from src.api.src.database.crud.private_courses_crud import PrivateCourseCRUD
from src.api.src.routers.api_enpoints import APIEndpoints
from src.api.src.utils.model_utils import ModelUtils


router = APIRouter()


@router.get(path=APIEndpoints.PrivateCourses.Get, status_code=status.HTTP_200_OK,
            response_model=ItemsDto[ScheduleCourseDto], summary="Get private courses for user.")
async def get_private_courses(user: UserContext, db: DbContext):
    if not user.has_any_role([Role.Tutor, Role.Student]):
        return ResponseBuilder.error_response(status.HTTP_403_FORBIDDEN, message="Access denied!")

    role = Role.Student if user.has_role(Role.Student) else Role.Tutor

    db_courses = PrivateCourseCRUD.get_private_courses(user.id, role, db)

    if not db_courses:
        return ResponseBuilder.success_response(content=ItemsDto(items=[]))

    items = ModelUtils.schedule_course_mapper(db_courses)

    return ResponseBuilder.success_response(content=ItemsDto[ScheduleCourseDto](items=items))


@router.get(path=APIEndpoints.PrivateCourses.GetBySubjects, status_code=status.HTTP_200_OK,
            response_model=ItemsDto[PrivateCourseInlineDto], summary="Get private courses for user by subject name")
async def get_private_courses(user_id: int, subject_name: str, role: Literal[Role.Tutor, Role.Student], user: UserContext, db: DbContext):
    private_courses = PrivateCourseCRUD.get_private_courses_by_subject(db, user_id, subject_name, role)

    if not private_courses:
        return ResponseBuilder.success_response(content=ItemsDto(items=[]))

    private_courses = [PrivateCourseInlineDto.from_tuple(pc) for pc in private_courses]

    return ResponseBuilder.success_response(content=ItemsDto[PrivateCourseInlineDto](items=private_courses))


@router.get(path=APIEndpoints.PrivateCourses.GetPrivateCourse, status_code=status.HTTP_200_OK,
            response_model=PrivateCourseDto[CourseMemberDto], summary="Get private courses by course id")
async def get_private_courses(private_course_id: int, user: UserContext, db: DbContext):
    private_course = PrivateCourseCRUD.get_private_course_by_course_id(db, private_course_id)

    if private_course is None:
        return ResponseBuilder.error_response(message="Course does not exist.")

    private_course = PrivateCourseDto[CourseMemberDto].model_validate(private_course)

    return ResponseBuilder.success_response(content=private_course)
