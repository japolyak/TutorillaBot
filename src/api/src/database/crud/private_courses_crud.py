from sqlalchemy import func, select, and_
from sqlalchemy.orm import Session, aliased, Mapped
from typing import Literal, Optional, Tuple

from src.core.models import Role

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
    def get_private_course_info(private_course_id: int, db: Session):
        student = aliased(User)
        tutor = aliased(User)

        private_course = (
            db
            .query(Subject.name, student.id, student.first_name, tutor.id, tutor.first_name)
            .join(PrivateCourse.tutor_course)
            .join(student, PrivateCourse.student)
            .join(TutorCourse.subject)
            .join(tutor, TutorCourse.tutor)
            .filter(PrivateCourse.id == private_course_id)
            .one_or_none()
        )

        return private_course

    @staticmethod
    def get_private_course_members(private_course_id: Mapped[int], db: Session) -> Optional[Tuple[int, int]]:
        return (
            db
            .query(PrivateCourse.student_id, TutorCourse.tutor_id)
            .join(PrivateCourse.tutor_course)
            .filter(PrivateCourse.id == private_course_id)
            .one_or_none()
        )


    @staticmethod
    def get_private_course_by_course_id(db: Session, private_course_id: int) -> PrivateCourse | None:
        # TODO - find solution how load ONLY some fields for Tutor and Student relations
        query = db.query(PrivateCourse).filter(PrivateCourse.id == private_course_id)

        return query.first()

    @staticmethod
    def private_course_exists(tutor_course_id: int, student_id, db: Session) -> bool:
        course = (
            db
            .query(PrivateCourse)
            .where(
                and_(
                    PrivateCourse.student_id == student_id,
                    PrivateCourse.tutor_course_id == tutor_course_id
                )
            )
            .first()
        )

        return course is not None
