from sqlalchemy import func, select
from sqlalchemy.orm import Session
from typing import Literal

from src.common.models import Role

from src.api.src.database.models import TutorCourse, Subject, PrivateCourse, User, PrivateClass


def get_private_courses(db: Session, user_id: int, subject_name: str, role: Literal[Role.Tutor, Role.Student]):
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


def get_private_course_by_course_id(db: Session, private_course_id: int) -> PrivateCourse | None:
    # TODO - find solution how load ONLY some fields for Tutor and Student relations
    query = db.query(PrivateCourse).filter(private_course_id == PrivateCourse.id)

    return query.first()


def enroll_student_to_course(db: Session, user_id: int, course_id: int) -> PrivateCourse:
    tutor_course = db.query(TutorCourse).filter(course_id == TutorCourse.id).first()

    private_course = PrivateCourse(student_id=user_id, tutor_course_id=course_id, price=tutor_course.price)
    db.add(private_course)
    db.commit()
    db.refresh(private_course)

    return private_course
