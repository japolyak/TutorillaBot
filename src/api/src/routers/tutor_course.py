from fastapi import status, APIRouter

from src.core.models import TutorCourseDto, NewTutorCourseDto, TutorCourseInlineDto, ItemsDto, UserDto, BlaTutorCourseDto, Role

from src.api.src.builders.response_builder import ResponseBuilder
from src.api.src.contexts.db_contex import DbContext
from src.api.src.contexts.user_context import UserContext
from src.api.src.database.crud.tutor_course_crud import TutorCourseCRUD
from src.api.src.database.crud.private_courses_crud import PrivateCourseCRUD
from src.api.src.routers.api_enpoints import APIEndpoints


router = APIRouter()


@router.post(path=APIEndpoints.TutorCourse.AddCourse, status_code=status.HTTP_201_CREATED,
             response_model=TutorCourseDto[UserDto], description="Add course for tutor")
async def add_course(new_tutor_course: NewTutorCourseDto, user_id: int, user: UserContext, db: DbContext):
    # TODO - rewrite
    new_tutor_course = TutorCourseCRUD.add_course(db=db, user_id=user_id, course=new_tutor_course)

    new_tutor_course = TutorCourseDto[UserDto].model_validate(new_tutor_course)

    return ResponseBuilder.success_response(content=new_tutor_course)


@router.get(path=APIEndpoints.TutorCourse.GetCourses, status_code=status.HTTP_200_OK,
             response_model=ItemsDto[BlaTutorCourseDto], description="Get tutor courses")
async def get_courses_ids(user_id: int, user: UserContext, db: DbContext):
    db_courses = TutorCourseCRUD.get_courses(db=db, user_id=user_id)

    if not db_courses:
        return ResponseBuilder.success_response(content=ItemsDto(items=[]))

    courses = [BlaTutorCourseDto(id=c[0], is_active=c[1], price=c[2], subject_name=c[3]) for c in db_courses]

    response_model = ItemsDto[BlaTutorCourseDto](items=courses)

    return ResponseBuilder.success_response(content=response_model)


@router.get(path=APIEndpoints.TutorCourse.GetBySubjectName, status_code=status.HTTP_200_OK,
            response_model=ItemsDto[TutorCourseInlineDto], description="Get available tutors")
async def get_available_tutor_courses(subject_name: str, user: UserContext, db: DbContext):
    if not user.has_role(Role.Student):
        return ResponseBuilder.error_response(status.HTTP_403_FORBIDDEN, message="Access denied!")

    db_tutor_courses = TutorCourseCRUD.get_available_courses_by_subject(user.id, subject_name, db)

    if not db_tutor_courses:
        return ResponseBuilder.success_response(content=ItemsDto(items=[]))

    tutor_courses = [
        TutorCourseInlineDto(id=tc[0], price=tc[1], subject_name=tc[2], tutor_name=tc[3]) for tc in db_tutor_courses
    ]

    response_model = ItemsDto[TutorCourseInlineDto](items=tutor_courses)

    return ResponseBuilder.success_response(content=response_model)


@router.post(path=APIEndpoints.TutorCourse.Enroll, status_code=status.HTTP_201_CREATED,
             summary="Enroll student to course")
async def enroll_in_course(tutor_course_id: int, user: UserContext, db: DbContext):
    if not user.has_role(Role.Student):
        return ResponseBuilder.error_response(status.HTTP_403_FORBIDDEN, message="Access denied!")

    private_course_exists = PrivateCourseCRUD.private_course_exists(tutor_course_id, user.id, db)
    if private_course_exists:
        return ResponseBuilder.error_response(message=f"User: {user.id} already enrolled in tutor course: {tutor_course_id}.")

    TutorCourseCRUD.enroll_student_to_course(user.id, tutor_course_id, db)

    return ResponseBuilder.success_response(status.HTTP_201_CREATED)
