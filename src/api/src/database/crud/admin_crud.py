from sqlalchemy import case, literal_column, func, select
from sqlalchemy.orm import Session
from typing import Literal

from src.common.models import Role

from src.api.src.database.models import UserRequest, User

class AdminCRUD:
    @staticmethod
    def get_users_requests(db: Session, role: Literal[Role.Tutor, Role.Student]):
        requested_role = case((UserRequest.student_role, literal_column(f"'{Role.Student}'")),
                              else_=literal_column(f"'{Role.Tutor}'"))

        query = (db.query(UserRequest.id, User.id, User.first_name, User.last_name, User.email, requested_role)
                 .join(UserRequest.user))

        if role == Role.Tutor:
            query = query.filter(UserRequest.tutor_role)
        else:
            query = query.filter(UserRequest.student_role)

        return query.all()

    @staticmethod
    def get_user_request(db: Session, request_id: int):
        requested_role = case((UserRequest.student_role, literal_column(f"'{Role.Student}'")),
                              else_=literal_column(f"'{Role.Tutor}'"))

        query = (db.query(UserRequest.id, User.id, User.first_name, User.last_name, User.email, requested_role)
                 .join(UserRequest.user)
                 .filter(request_id == UserRequest.id))

        return query.first()

    @staticmethod
    def requests_statistics(db: Session):
        query = db.execute(
            select(
                func.count().filter(UserRequest.student_role == True).label("students"),
                func.count().filter(UserRequest.tutor_role == True).label("tutors"),
            )
            .select_from(UserRequest)
        )

        return query.first()
