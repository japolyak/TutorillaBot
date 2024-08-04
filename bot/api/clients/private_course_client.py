import requests
from bot.config import api_link


class PrivateCourseClient:
    __link = f"{api_link}/private-courses"

    @classmethod
    def get_classes(cls, private_course_id: int, role: str, user_id: int, page: int = 1):
        url = f"{cls.__link}/{private_course_id}/classes/?role={role}&page={page}&user_id={user_id}"
        r = requests.get(url)

        return r

    @classmethod
    def get_private_courses_by_course_name(cls, user_id: int, subject_name: str, role: str):
        url = f"{cls.__link}/users/{user_id}/subjects/{subject_name}/?role={role}"
        r = requests.get(url)

        return r

    @classmethod
    def enroll_in_course(cls, user_id: int, private_course_id: int):
        url = f"{cls.__link}/{private_course_id}/users/{user_id}/"
        r = requests.post(url)

        return r
