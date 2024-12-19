from sqlalchemy.orm import Session

from src.api.src.database.models import TutorCourse, Subject, PrivateCourse


class SubjectsCrud:
    @staticmethod
    def get_available_subjects(user_id: int, db: Session):
        private_courses_subquery = (
            db.query(PrivateCourse.tutor_course_id)
            .filter(PrivateCourse.student_id == user_id)
            .subquery()
        )

        return (
            db.query(Subject)
            .join(Subject.tutor_courses)
            .filter(TutorCourse.is_active)
            .filter(TutorCourse.tutor_id != user_id)
            .filter(TutorCourse.id.notin_(private_courses_subquery))
            .distinct()
            .all()
        )

    # @staticmethod
    # def get_student_subjects(user_id: int, available: bool, db: Session):
    #     sub_query = (select(1)
    #                  .select_from(PrivateCourse)
    #                  .filter(PrivateCourse.tutor_course_id == TutorCourse.id, user_id == PrivateCourse.student_id)
    #                  .exists())
    #
    #     query = (db.query(Subject)
    #              .join(Subject.tutor_courses)
    #              .filter(user_id != TutorCourse.tutor_id,
    #                      ~sub_query if available else sub_query))
    #
    #     if available:
    #         query = query.filter(TutorCourse.is_active)
    #
    #     return query.all()
    #
    # @staticmethod
    # def get_tutor_subjects(db: Session, user_id: int, available: bool):
    #     sub_query = (select(1)
    #                  .select_from(TutorCourse)
    #                  .filter(user_id == TutorCourse.tutor_id, TutorCourse.subject_id == Subject.id)
    #                  .exists())
    #
    #     query = db.query(Subject).filter(~sub_query if available else sub_query)
    #
    #     return query.all()
