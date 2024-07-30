import requests
from src.bot.config import api_link


class TutorCourseClient:
    __link = f"{api_link}/tutor-courses"

    @classmethod
    def add_course(cls, user_id: int, payload):
        url = f"{cls.__link}/users/{user_id}/"
        r = requests.post(url, data=payload)

        return r

    @classmethod
    def course_tutors(cls, user_id: int, subject_name: str):
        url = f"{cls.__link}/users/{user_id}/subject-name/{subject_name}/"
        r = requests.get(url)

        return r
