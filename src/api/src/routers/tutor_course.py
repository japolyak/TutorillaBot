from fastapi import status, APIRouter, Depends
from sqlalchemy.orm import Session

from src.common.models import TutorCourseDto, NewTutorCourseDto, TutorCourseInlineDto, ItemsDto, UserDto, BlaTutorCourseDto

from src.api.src.builders.response_builder import ResponseBuilder
from src.api.src.database.crud import tutor_course_crud
from src.api.src.database.db_setup import session
from src.api.src.routers.api_enpoints import APIEndpoints


router = APIRouter()


@router.post(path=APIEndpoints.TutorCourse.AddCourse, status_code=status.HTTP_201_CREATED,
             response_model=TutorCourseDto[UserDto], description="Add course for tutor")
async def add_course(new_tutor_course: NewTutorCourseDto, user_id: int, db: Session = Depends(session)):
    # TODO - rewrite
    new_tutor_course = tutor_course_crud.add_course(db=db, user_id=user_id, course=new_tutor_course)

    new_tutor_course = TutorCourseDto[UserDto].model_validate(new_tutor_course)

    return ResponseBuilder.success_response(content=new_tutor_course)


@router.get(path=APIEndpoints.TutorCourse.GetCourses, status_code=status.HTTP_200_OK,
             response_model=ItemsDto[BlaTutorCourseDto], description="Get tutor courses")
async def get_courses_ids(user_id: int, db: Session = Depends(session)):
    db_courses = tutor_course_crud.get_courses(db=db, user_id=user_id)

    if not db_courses:
        return ResponseBuilder.success_response(content=ItemsDto(items=[]))

    courses = [BlaTutorCourseDto(id=c[0], is_active=c[1], price=c[2], subject_name=c[3]) for c in db_courses]

    response_model = ItemsDto[BlaTutorCourseDto](items=courses)

    return ResponseBuilder.success_response(content=response_model)


@router.get(path=APIEndpoints.TutorCourse.AvailableCourses, status_code=status.HTTP_200_OK,
            response_model=ItemsDto[TutorCourseInlineDto], description="Get available tutors")
async def get_available_tutor_courses(user_id: int, subject_name: str, db: Session = Depends(session)):
    db_tutor_courses = tutor_course_crud.get_available_courses_by_subject(db=db, user_id=user_id, subject_name=subject_name)

    if not db_tutor_courses:
        return ResponseBuilder.success_response(content=ItemsDto(items=[]))

    tutor_courses = [
        TutorCourseInlineDto(id=tc[0], price=tc[1], subject_name=tc[2], tutor_name=tc[3]) for tc in db_tutor_courses
    ]

    response_model = ItemsDto[TutorCourseInlineDto](items=tutor_courses)

    return ResponseBuilder.success_response(content=response_model)
