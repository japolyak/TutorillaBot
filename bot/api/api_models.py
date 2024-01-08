from pydantic import BaseModel
from typing import List
from datetime import datetime


class UserDto(BaseModel):
    id: int
    first_name: str
    last_name: str
    email: str
    normalized_email: str
    phone_number: str
    is_tutor: bool
    is_student: bool
    is_admin: bool


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
    student: User
    course: TutorCourse
