from sqlalchemy.orm import Session

from src.core.models import NewTutorCourseDto

from src.api.src.database.models import TutorCourse, Subject, User, PrivateCourse


class TutorCourseCRUD:
    @staticmethod
    def add_course(db: Session, user_id: int, course: NewTutorCourseDto) -> TutorCourse:
        db_course = TutorCourse(tutor_id=user_id, subject_id=course.subject_id, price=course.price)
        db.add(db_course)
        db.commit()
        db.refresh(db_course)

        return db_course

    @staticmethod
    def get_courses(db: Session, user_id: int):
        query = (
            db.query(TutorCourse.id, TutorCourse.is_active, TutorCourse.price, Subject.name)
            .join(TutorCourse.subject)
            .filter(user_id == TutorCourse.tutor_id)
        )

        return query.all()

    @staticmethod
    def get_available_courses_by_subject(user_id: int, subject_name: str, db: Session):
        private_courses_subquery = (
            db.query(PrivateCourse.tutor_course_id)
            .filter(PrivateCourse.student_id == user_id)
            .subquery()
        )

        query = (
            db.query(TutorCourse.id, TutorCourse.price, Subject.name, User.first_name)
            .join(TutorCourse.subject)
            .join(TutorCourse.tutor)
            .filter(TutorCourse.is_active)
            .filter(TutorCourse.tutor_id != user_id)
            .filter(Subject.name == subject_name)
            .filter(TutorCourse.id.notin_(private_courses_subquery))
        )

        return query.all()

    @staticmethod
    def enroll_student_to_course(user_id: int, tutor_course_id: int, db: Session, ) -> PrivateCourse:
        tutor_course = db.query(TutorCourse).filter(TutorCourse.id == tutor_course_id).first()

        private_course = PrivateCourse(student_id=user_id, tutor_course_id=tutor_course_id, price=tutor_course.price)
        db.add(private_course)
        db.commit()
        db.refresh(private_course)

        return private_course
