from pydantic import BaseModel
from typing import List, Generic, TypeVar
from datetime import datetime
from enum import StrEnum


T = TypeVar('T')


class Role(StrEnum):
    Admin = 'admin'
    Tutor = 'tutor'
    Student = 'student'


class PaginatedList(BaseModel, Generic[T]):
    items: List[T]
    total: int
    current_page: int
    pages: int

    class Config:
        from_attributes = True


class UserBaseDto(BaseModel):
    locale: str
    id: int
    first_name: str
    last_name: str
    email: str
    time_zone: float


class UserDto(UserBaseDto):
    normalized_email: str
    is_active: bool
    is_tutor: bool
    is_student: bool
    is_admin: bool


class UserRequestDto(BaseModel):
    id: int
    request_datetime: datetime
    user: UserDto
    tutor_role: bool
    student_role: bool


class SubjectDto(BaseModel):
    id: int
    name: str


class TutorCourseDto(BaseModel):
    id: int
    tutor: UserDto
    subject: SubjectDto
    is_active: bool
    price: int


class PrivateCourseDto(BaseModel):
    id: int
    student: UserDto
    course: TutorCourseDto
    price: int


class SourceDto(BaseModel):
    title: str
    assignment: str


class PrivateClassBaseDto(BaseModel):
    id: int
    schedule_datetime: datetime
    assignment: List[SourceDto]
    is_scheduled: bool
    has_occurred: bool
    is_paid: bool


# TODO - rename model
class PrivateClassDto(BaseModel):
    private_course: PrivateCourseDto
    classes: List[PrivateClassBaseDto]


class NewTutorCourseDto(BaseModel):
    subject_id: int
    price: int

    class Config:
        from_attributes = True
