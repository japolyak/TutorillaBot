from sqlalchemy.orm import Session
from typing import List, Type

from src.api.src.database.models import Textbook


class TextbookCRUD:
    @staticmethod
    def get_textbooks(db: Session, tutor_course_id: int) -> List[Textbook]:
        query = db.query(Textbook).where(Textbook.tutor_course_id == tutor_course_id)

        return query.all()

    @staticmethod
    def create_textbooks(db: Session, tutor_course_id: int, titles: List[str]):
        for title in titles:
            textbook = Textbook(title=title, tutor_course_id=tutor_course_id)
            db.add(textbook)

        db.commit()

    @staticmethod
    def delete_textbook(db: Session, textbook_id: int):
        db_textbook = db.query(Textbook).filter(textbook_id == Textbook.id).first()

        if db_textbook is None:
            return False

        db.delete(db_textbook)
        db.commit()

        return True
