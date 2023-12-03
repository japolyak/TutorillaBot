from ..api.api_models import TutorCourse, Subject, User, PrivateCourse
from typing import List


class UserSerializer:
    @staticmethod
    def serialize(user) -> User:
        return User(user['id'], user['first_name'], user['last_name'], user['email'], user['email'],
                    user['phone_number'], user['is_tutor'], user['is_student'], user['is_admin'])


class SubjectSerializer:
    @staticmethod
    def serialize(subject: list) -> List[Subject]:
        subjects: List[Subject] = []

        for s in subject:
            subject = Subject(s['id'], s['name'])
            subjects.append(subject)

        return subjects


class TutorCourseSerializer:
    @staticmethod
    def serialize(course: list) -> List[TutorCourse]:
        tutor_courses: List[TutorCourse] = []

        for c in course:
            tutor = User(c['tutor']['id'], c['tutor']['first_name'], c['tutor']['last_name'],
                         c['tutor']['email'], c['tutor']['normalized_email'], c['tutor']['phone_number'],
                         c['tutor']['is_tutor'], c['tutor']['is_student'], c['tutor']['is_admin'])
            subject = Subject(c['subject']['id'], c['subject']['name'])
            tutor_course = TutorCourse(c['id'], c['is_active'], subject, tutor)

            tutor_courses.append(tutor_course)

        return tutor_courses


class PrivateCourseSerializer:
    @staticmethod
    def serialize(course: list) -> List[PrivateCourse]:
        private_courses: List[PrivateCourse] = []

        for c in course:
            student = User(c['student']['id'], c['student']['first_name'],
                           c['student']['last_name'], c['student']['email'],
                           c['student']['normalized_email'], c['student']['phone_number'],
                           c['student']['is_tutor'], c['student']['is_student'],
                           c['student']['is_admin'])

            subject = Subject(c['course']['subject']['id'], c['course']['subject']['name'])

            tutor = User(c['course']['tutor']['id'], c['course']['tutor']['first_name'],
                         c['course']['tutor']['last_name'], c['course']['tutor']['email'],
                         c['course']['tutor']['normalized_email'], c['course']['tutor']['phone_number'],
                         c['course']['tutor']['is_tutor'], c['course']['tutor']['is_student'],
                         c['course']['tutor']['is_admin'])

            tutor_course = TutorCourse(c['course']['id'], c['course']['is_active'], subject, tutor)

            private_course = PrivateCourse(c['id'], student, tutor_course)
            private_courses.append(private_course)

        return private_courses
