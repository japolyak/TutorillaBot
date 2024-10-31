from fastapi import status, APIRouter
from typing import Literal

from src.common.models import SubjectDto, Role, ItemsDto

from src.api.src.builders.response_builder import ResponseBuilder
from src.api.src.database.crud import subject_crud
from src.api.src.database.db_setup import DbContext
from src.api.src.routers.api_enpoints import APIEndpoints


router = APIRouter()


@router.get(path=APIEndpoints.Subjects.Get, status_code=status.HTTP_200_OK,
            summary="Gets users subjects by user id", response_model=ItemsDto[SubjectDto])
async def get_subjects(user_id: int, is_available: bool, role: Literal[Role.Student, Role.Tutor], db: DbContext):
    role_to_function = {
        Role.Student: subject_crud.get_student_subjects,
        Role.Tutor: subject_crud.get_tutor_subjects
    }

    subjects_func = role_to_function.get(role)

    subjects = subjects_func(db, user_id, is_available)

    if not subjects:
        return ResponseBuilder.success_response(content=ItemsDto(items=[]))

    mapped_subjects = [SubjectDto(id=subject.id, name=subject.name) for subject in subjects]

    return ResponseBuilder.success_response(content=ItemsDto(items=mapped_subjects))
