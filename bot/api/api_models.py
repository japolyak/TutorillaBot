from pydantic import BaseModel


class User(BaseModel):
    id: int
    first_name: str
    last_name: str
    email: str
    normalized_email: str
    phone_number: str
    is_tutor: bool
    is_student: bool
    is_admin: bool


class Subject(BaseModel):
    id: int
    name: str


class TutorCourse(BaseModel):
    id: int
    tutor: User
    subject: Subject
    is_active: bool


class PrivateCourse(BaseModel):
    id: int
    student: User
    course: TutorCourse
