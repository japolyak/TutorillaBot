from typing import List
from sqlalchemy.orm import Session

from src.api.src.utils.token_utils import UserContextModel


class IValidator:
    _errors: List[str] = []

    def __init__(self, user: UserContextModel, db: Session):
        self._user = user
        self._db = db

    @property
    def is_valid(self):
        return len(self._errors) == 0

    @property
    def errors(self):
        return self._errors
