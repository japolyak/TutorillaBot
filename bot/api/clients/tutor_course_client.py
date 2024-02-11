import requests
from bot.config import api_link


class TutorCourseClient:
    @staticmethod
    def add_course(user_id: int, subject_id: int):
        url = f"{api_link}/tutor-courses/users/{user_id}/subjects/{subject_id}/"
        r = requests.post(url)

        return r

    @staticmethod
    def course_tutors(user_id: int, subject_name: str):
        url = f"{api_link}/tutor-courses/users/{user_id}/subject-name/{subject_name}/"
        r = requests.get(url)

        return r
