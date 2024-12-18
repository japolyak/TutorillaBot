from typing import Literal
from sqlalchemy.orm import Session
import time

from src.api.src.database.models import UserRequest
from src.core.models import Role


class UserRequestCRUD:
    @staticmethod
    def create_user_request(user_id: int, role: Literal[Role.Tutor, Role.Student], db: Session) -> bool:
        role = 1 if role == Role.Tutor else 2
        request_time = int(time.time()) * 1000

        new_user_request = UserRequest(user_id=user_id, role=role, request_time_unix=request_time)

        db.add(new_user_request)
        db.commit()
        db.refresh(new_user_request)

        return new_user_request is not None
