from typing import Optional
from sqlalchemy.orm import Session

from src.api.src.database.models import User, UserRequest
from src.core.models import UserBaseDto


class UserCRUD:
    @staticmethod
    def get_user(user_id: int, db: Session) -> Optional[User]:
        return db.query(User).filter(User.id == user_id).one_or_none()

    @staticmethod
    def create_user(user: UserBaseDto, db: Session) -> bool:
        new_user = User(id=user.id, first_name=user.first_name, last_name=user.last_name, email=user.email, normalized_email=user.email.lower(), time_zone=user.time_zone, locale=user.locale)

        db.add(new_user)
        db.commit()
        db.refresh(new_user)

        return new_user is not None

    @staticmethod
    def get_user_by_request_id(db: Session, request_id: int) -> User | None:
        user = db.query(User).join(UserRequest).filter(UserRequest.id == request_id).first()

        return user

    @staticmethod
    def accept_role_request(db: Session, request_id: int, user: User) -> Optional[UserRequest]:
        db_user_request = db.query(UserRequest).filter(UserRequest.id == request_id).first()

        if db_user_request is None: return None

        # TODO - rethink...
        if db_user_request.role == 2:
            user.is_student = True
        elif db_user_request.role == 1:
            user.is_tutor = True

        user.is_active = True

        return db_user_request

    @staticmethod
    def decline_role_request(db: Session, request_id: int) -> bool:
        db_user_request = db.query(UserRequest).filter(UserRequest.id == request_id).first()

        if db_user_request is None:
            return False

        db.delete(db_user_request)
        db.commit()

        return True
