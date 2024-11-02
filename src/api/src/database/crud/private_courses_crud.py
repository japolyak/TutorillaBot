from sqlalchemy import func, select
from sqlalchemy.orm import Session
from typing import Literal

from src.common.models import Role

from src.api.src.database.models import TutorCourse, Subject, PrivateCourse, User, PrivateClass


class PrivateCourseCRUD:
    @staticmethod
    def get_private_courses(user_id: int, role: Literal[Role.Tutor, Role.Student], db: Session):
        courses = []

        base_query = (
            db.query(
                Subject.id.label('subject_id'),
                Subject.name.label('subject_name'),
                PrivateCourse.id.label('course_id'),
                User.id.label('user_id'),
                User.first_name.label('user_first_name'),
                User.time_zone.label('user_time_zone')
            )
            .join(PrivateCourse.tutor_course)
            .join(TutorCourse.subject)
        )

        if role == Role.Tutor:
            courses = (
                base_query
                .join(PrivateCourse.student)
                .filter(user_id == TutorCourse.tutor_id)
            ).order_by(PrivateCourse.id).all()
        elif role == Role.Student:
            courses = (
                base_query
                .join(TutorCourse.tutor)
                .filter(user_id == PrivateCourse.student_id)
            ).order_by(PrivateCourse.id).all()

        return courses

    @staticmethod
    def get_private_courses_by_subject(db: Session, user_id: int, subject_name: str, role: Literal[Role.Tutor, Role.Student]):
        sub_query = (
            select(func.count())
            .where(PrivateClass.private_course_id == PrivateCourse.id)
            .correlate(PrivateCourse)
            .as_scalar()
        )

        query = (db.query(
            PrivateCourse.id,
            Subject.name,
            User.first_name,
            sub_query
        )
                 .join(PrivateCourse.tutor_course)
                 .join(TutorCourse.subject)
                 .filter(subject_name == Subject.name))

        if role == Role.Student:
            query = query.join(TutorCourse.tutor).filter(user_id == PrivateCourse.student_id)
        else:
            query = query.join(PrivateCourse.student).filter(user_id == TutorCourse.tutor_id)

        return query.all()

    @staticmethod
    def get_private_course_by_course_id(db: Session, private_course_id: int) -> PrivateCourse | None:
        # TODO - find solution how load ONLY some fields for Tutor and Student relations
        query = db.query(PrivateCourse).filter(private_course_id == PrivateCourse.id)

        return query.first()

    @staticmethod
    def enroll_student_to_course(db: Session, user_id: int, course_id: int) -> PrivateCourse:
        tutor_course = db.query(TutorCourse).filter(course_id == TutorCourse.id).first()

        private_course = PrivateCourse(student_id=user_id, tutor_course_id=course_id, price=tutor_course.price)
        db.add(private_course)
        db.commit()
        db.refresh(private_course)

        return private_course
