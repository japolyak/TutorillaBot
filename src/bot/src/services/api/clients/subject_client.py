import requests
from typing import Literal

from src.common.config import api_link
from src.common.models import Role


class SubjectClient:
    __link = f"{api_link}/subjects"

    @classmethod
    def get_users_subjects(cls, user_id: int, role: Literal[Role.Student, Role.Tutor], is_available: bool):
        url = f"{cls.__link}/users/{user_id}/available/{is_available}/?role={role}"
        r = requests.get(url, timeout=15)

        return r
