from typing import Annotated
from fastapi import Depends
from sqlalchemy.orm import Session

from src.api.src.database.db_setup import SessionLocal


def session():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

DbContext = Annotated[Session, Depends(session)]
