from pydantic import BaseModel
from typing import List
from datetime import datetime


class UserBaseDto(BaseModel):
    id: int
    first_name: str
    last_name: str
    email: str
    phone_number: str
    time_zone: int


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


class PrivateCourseDto(BaseModel):
    id: int
    student: UserDto
    course: TutorCourseDto


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
