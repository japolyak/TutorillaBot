class User:
    def __init__(self, user_id: int, first_name: str, last_name: str, email: str, normalized_email: str,
                 phone_number: str, is_tutor: bool, is_student: bool, is_admin: bool):
        self.id = user_id
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.normalized_email = normalized_email
        self.phone_number = phone_number
        self.is_tutor = is_tutor
        self.is_student = is_student
        self.is_admin = is_admin


class Subject:
    def __init__(self, subject_id: int, name: str):
        self.id = subject_id
        self.name = name


class TutorCourse:
    def __init__(self, tutor_course_id: int, is_active: bool, subject: Subject, tutor: User):
        self.id = tutor_course_id
        self.tutor = tutor
        self.subject = subject
        self.is_active = is_active


class PrivateCourse:
    def __init__(self, private_course_id: int, student: User, course: TutorCourse):
        self.id = private_course_id
        self.student = student
        self.course = course
