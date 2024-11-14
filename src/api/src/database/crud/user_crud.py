from sqlalchemy.orm import Session

from src.api.src.database.models import User, UserRequest


class UserCRUD:
    @staticmethod
    def get_user(db: Session, user_id: int) -> User | None:
        user = db.query(User).filter(User.id == user_id).first()

        return user

    @staticmethod
    def get_user_by_request_id(db: Session, request_id: int) -> User | None:
        user = db.query(User).join(UserRequest).filter(UserRequest.id == request_id).first()

        return user

    @staticmethod
    def accept_role_request(db: Session, request_id: int, user: User):
        return True
        db_user_request = db.query(UserRequest).filter(UserRequest.id == request_id).first()

        if db_user_request is None:
            return None

        if db_user_request.role == 2:
            user.is_student = True
        elif db_user_request.role == 1:
            user.is_tutor = True

        user.is_active = True

        db.delete(db_user_request)
        db.commit()
        db.refresh(user)

        return user

    @staticmethod
    def decline_role_request(db: Session, request_id: int) -> bool:
        db_user_request = db.query(UserRequest).filter(UserRequest.id == request_id).first()

        if db_user_request is None:
            return False

        db.delete(db_user_request)
        db.commit()

        return True
