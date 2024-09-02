from pydantic import BaseModel
from typing import List, Generic, TypeVar, Tuple
from datetime import datetime
from enum import StrEnum
from pydantic.alias_generators import to_camel


T = TypeVar('T')


class BaseDto(BaseModel):
    class Config:
        from_attributes = True
        # Next 2 convert snake_case to camelCase
        populate_by_name = True
        alias_generator = to_camel


class ClassStatus(StrEnum):
    Scheduled = 'Scheduled'
    Occurred = 'Occurred'
    Paid = 'Paid'


class Role(StrEnum):
    Admin = 'Admin'
    Tutor = 'Tutor'
    Student = 'Student'


class PaginatedList(BaseModel, Generic[T]):
    items: List[T]
    total: int
    current_page: int
    pages: int

    class Config:
        from_attributes = True


class ItemsDto(BaseDto, Generic[T]):
    items: List[T]


class ErrorDto(BaseModel):
    detail: str

    class Config:
        from_attributes = True


class UserBaseDto(BaseDto):
    id: int
    first_name: str
    last_name: str
    email: str
    time_zone: float
    locale: str


class UserDto(UserBaseDto):
    normalized_email: str | None = None
    is_active: bool | None = None
    is_tutor: bool | None = None
    is_student: bool | None = None
    is_admin: bool | None = None


class UserRequestDto(BaseModel):
    id: int
    user_id: int
    user_first_name: str
    user_last_name: str
    user_email: str
    user_role: Role

    class Config:
        from_attributes = True


class SubjectDto(BaseDto):
    id: int
    name: str


class TutorCourseInlineDto(BaseModel):
    id: int
    tutor_name: str
    subject_name: str
    price: int

    class Config:
        from_attributes = True


class TextbookDto(BaseDto):
    id: int
    title: str


class CourseMemberDto(BaseDto):
    id: int
    first_name: str


class TutorCourseDto(BaseDto, Generic[T]):
    id: int
    tutor: T
    subject: SubjectDto
    textbooks: List[TextbookDto]
    is_active: bool
    price: int


class PrivateCourseDto(BaseDto, Generic[T]):
    id: int
    tutor_course: TutorCourseDto[T]
    student: T
    price: int


class PrivateCourseInlineDto(BaseModel):
    id: int
    person_name: str
    subject_name: str
    number_of_classes: int

    @classmethod
    def from_tuple(cls, values: Tuple[int, str, str, int]):
        if len(values) != 4:
            raise ValueError("List must contain exactly two elements: [name, age]")

        return cls(id=values[0], person_name=values[1], subject_name=values[2], number_of_classes=values[3])

    class Config:
        from_attributes = True


class AssignmentDto(BaseDto):
    textbook_id: int
    description: str


class NewClassDto(BaseDto):
    date: datetime
    assignments: List[AssignmentDto]


class PrivateClassDto(BaseModel):
    id: int
    schedule_datetime: datetime
    status: ClassStatus

    class Config:
        from_attributes = True


# class PrivateClassBaseDto(BaseModel):
#     id: int
#     schedule_datetime: datetime
#     assignment: List[SourceDto]
#     is_scheduled: bool
#     has_occurred: bool
#     is_paid: bool
#
#     class Config:
#         from_attributes = True


class NewTutorCourseDto(BaseModel):
    subject_id: int
    price: int

    class Config:
        from_attributes = True


class ClassDto(BaseDto):
    date: datetime
    status: ClassStatus


class NewTextbooksDto(BaseDto):
    tutor_course_id: int
    titles: List[str]
