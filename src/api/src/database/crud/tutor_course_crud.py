from sqlalchemy.orm import Session

from src.common.models import NewTutorCourseDto

from src.api.src.database.models import TutorCourse, Subject, User, Textbook


def add_course(db: Session, user_id: int, course: NewTutorCourseDto):

    db_course = TutorCourse(tutor_id=user_id, subject_id=course.subject_id, price=course.price)
    db.add(db_course)
    db.commit()
    db.refresh(db_course)

    return db_course


def get_available_courses_by_subject(db: Session, user_id: int, subject_name: str):
    query = (
        db.query(TutorCourse.id, TutorCourse.price, Subject.name, User.first_name)
        .join(TutorCourse.subject)
        .join(TutorCourse.tutor)
        .filter(subject_name == Subject.name, TutorCourse.is_active, user_id != TutorCourse.tutor_id)
    )

    return query.all()


def get_tutor_course_textbooks(db: Session, tutor_course_id: int):
    query = db.query(Textbook.id, Textbook.title).filter(tutor_course_id == Textbook.tutor_course_id)

    return query.all()
