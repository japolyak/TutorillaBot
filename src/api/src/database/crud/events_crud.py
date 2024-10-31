from sqlalchemy.orm import Session
from sqlalchemy import and_
from typing import List, Literal

from src.api.src.database.models import PrivateClass
from src.common.models import Role


class EventCRUD:
    @staticmethod
    def create_class_event(db: Session, private_course_id: int, start_time_unix: int, duration: int) -> PrivateClass:
        new_class = PrivateClass(private_course_id=private_course_id, start_time_unix=start_time_unix, duration=duration)

        db.add(new_class)
        db.commit()
        db.refresh(new_class)

        return new_class

    @staticmethod
    def get_events_between_dates(db: Session, user_id: int, role: Literal[Role.Tutor, Role.Student], start_time_unix: int, end_time_unix: int) -> List[PrivateClass]:
        classes = db.query(PrivateClass).where(
            and_(
                start_time_unix <= PrivateClass.start_time_unix,
                end_time_unix >= PrivateClass.start_time_unix
            )
        ).all()

        return classes
