from sqlalchemy import case, literal_column, func, select
from sqlalchemy.orm import Session
from typing import Literal

from src.common.models import Role

from src.api.src.database.models import UserRequest, User

class AdminCRUD:
    @staticmethod
    def get_users_requests(db: Session, role: Literal[Role.Tutor, Role.Student]):
        requested_role = case((2 == UserRequest.role, literal_column(f"'{Role.Student}'")),
                              else_=literal_column(f"'{Role.Tutor}'"))

        query = (db.query(UserRequest.id, User.id, User.first_name, User.last_name, User.email, requested_role)
                 .join(UserRequest.user))

        if role == Role.Tutor:
            query = query.filter(1 == UserRequest.role)
        else:
            query = query.filter(2 == UserRequest.role)

        return query.all()

    @staticmethod
    def requests_statistics(db: Session):
        query = db.execute(
            select(
                func.count().filter(UserRequest.role == 2).label("students"),
                func.count().filter(UserRequest.role == 1).label("tutors"),
            )
            .select_from(UserRequest)
        )

        return query.first()
