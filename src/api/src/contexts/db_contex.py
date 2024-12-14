from typing import Annotated
from fastapi import Depends
from sqlalchemy.orm import Session

from src.api.src.database.db_manager import db_manager


def session():
    db = db_manager.session

    try:
        yield db
    finally:
        db.close()

DbContext = Annotated[Session, Depends(session)]
