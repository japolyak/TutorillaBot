from fastapi import status, APIRouter
from typing import Literal

from src.common.models import (PaginatedList, Role, PrivateCourseInlineDto, ItemsDto,
                               PrivateClassDto, PrivateCourseDto, CourseMemberDto, ScheduleCourseDto)

from src.api.src.builders.response_builder import ResponseBuilder
from src.api.src.database.crud.private_courses_crud import PrivateCourseCRUD
from src.api.src.database.db_setup import DbContext
from src.api.src.utils.token_utils import UserContext
from src.api.src.functions.time_transformator import transform_class_time
from src.api.src.routers.api_enpoints import APIEndpoints
from src.api.src.utils.model_utils import ModelUtils


router = APIRouter()


# @router.get(path=APIEndpoints.PrivateCourses.GetClasses, status_code=status.HTTP_200_OK,
#             response_model=PaginatedList[PrivateClassDto], summary="Get classes of the course")
# async def get_classes_for_bot(course_id: int, user_id: int, role: Literal[Role.Tutor, Role.Student], page: int, db: DbContext):
#     result = db.execute(sql_statements.get_classes, {"p1": user_id, "p2": course_id, "p3": page, "p4": role}).fetchall()
#
#     total_count = None
#     user_timezone = None
#     classes: list[PrivateClassDto] = []
#
#     for row in result:
#         if row[0] is None:
#             return ResponseBuilder.error_response(message=row[4])
#
#         if total_count is None or user_timezone is None:
#             total_count = row[1]
#             user_timezone = row[3]
#
#         new_time = transform_class_time(row[2], row[3])
#
#         private_class = PrivateClassDto(id=row[0], schedule_datetime=new_time, status=row[4])
#         classes.append(private_class)
#
#     pages = total_count // 3 + (0 if total_count % 3 == 0 else 1)
#
#     response_model = PaginatedList[PrivateClassDto](
#         items=classes,
#         total=total_count,
#         current_page=page,
#         pages=pages)
#
#     return ResponseBuilder.success_response(content=response_model)


@router.get(path=APIEndpoints.PrivateCourses.Get, status_code=status.HTTP_200_OK,
            response_model=ItemsDto[ScheduleCourseDto], summary="Get private courses for user.")
async def get_private_courses(user: UserContext, db: DbContext):
    if user.role not in [Role.Tutor, Role.Student]:
        return ResponseBuilder.error_response(status.HTTP_403_FORBIDDEN, message="Access denied!")

    db_courses = PrivateCourseCRUD.get_private_courses(user.id, user.role, db)

    if not db_courses:
        return ResponseBuilder.success_response(content=ItemsDto(items=[]))

    items = ModelUtils.schedule_course_mapper(db_courses)

    return ResponseBuilder.success_response(content=ItemsDto[ScheduleCourseDto](items=items))


@router.get(path=APIEndpoints.PrivateCourses.GetBySubjects, status_code=status.HTTP_200_OK,
            response_model=ItemsDto[PrivateCourseInlineDto], summary="Get private courses for user by subject name")
async def get_private_courses(user_id: int, subject_name: str, role: Literal[Role.Tutor, Role.Student], db: DbContext):
    private_courses = PrivateCourseCRUD.get_private_courses_by_subject(db, user_id, subject_name, role)

    if not private_courses:
        return ResponseBuilder.success_response(content=ItemsDto(items=[]))

    private_courses = [PrivateCourseInlineDto.from_tuple(pc) for pc in private_courses]

    return ResponseBuilder.success_response(content=ItemsDto[PrivateCourseInlineDto](items=private_courses))


@router.post(path=APIEndpoints.PrivateCourses.Enroll, status_code=status.HTTP_201_CREATED,
             summary="Enroll student to course")
async def enroll_in_course(user_id: int, private_course_id: int, db: DbContext):
    # TODO: Rewrite
    PrivateCourseCRUD.enroll_student_to_course(db=db, user_id=user_id, course_id=private_course_id)
    return ResponseBuilder.success_response(status.HTTP_201_CREATED)


@router.get(path=APIEndpoints.PrivateCourses.GetPrivateCourse, status_code=status.HTTP_200_OK,
            response_model=PrivateCourseDto[CourseMemberDto], summary="Get private courses by course id")
async def get_private_courses(private_course_id: int, db: DbContext):
    private_course = PrivateCourseCRUD.get_private_course_by_course_id(db, private_course_id)

    if private_course is None:
        return ResponseBuilder.error_response(message="Course does not exist.")

    private_course = PrivateCourseDto[CourseMemberDto].model_validate(private_course)

    return ResponseBuilder.success_response(content=private_course)
