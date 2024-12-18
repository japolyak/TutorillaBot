from sqlalchemy.orm import Session

from src.core.models import NewTutorCourseDto

from src.api.src.database.models import TutorCourse, Subject, User


def add_course(db: Session, user_id: int, course: NewTutorCourseDto) -> TutorCourse:
    db_course = TutorCourse(tutor_id=user_id, subject_id=course.subject_id, price=course.price)
    db.add(db_course)
    db.commit()
    db.refresh(db_course)

    return db_course


def get_courses(db: Session, user_id: int):
    query = (
        db.query(TutorCourse.id, TutorCourse.is_active, TutorCourse.price, Subject.name)
        .join(TutorCourse.subject)
        .filter(user_id == TutorCourse.tutor_id)
    )

    return query.all()


def get_available_courses_by_subject(db: Session, user_id: int, subject_name: str):
    query = (
        db.query(TutorCourse.id, TutorCourse.price, Subject.name, User.first_name)
        .join(TutorCourse.subject)
        .join(TutorCourse.tutor)
        .filter(subject_name == Subject.name, TutorCourse.is_active, user_id != TutorCourse.tutor_id)
    )

    return query.all()
