import requests
from bot.config import api_link


class StudentClient:
    @staticmethod
    def available_courses_student(user_id: int):
        url = f"{api_link}/students/{user_id}/available-courses/"
        r = requests.get(url)

        return r

    @staticmethod
    def my_classes(user_id: int):
        url = f"{api_link}/students/{user_id}/courses/"
        r = requests.get(url)

        return r

    @staticmethod
    def enroll_in_course(user_id: int, course_id: int):
        url = f"{api_link}/students/{user_id}/courses/{course_id}/"
        r = requests.post(url)

        return r

    @staticmethod
    def course_tutors(user_id: int, subject_name: str):
        url = f"{api_link}/students/{user_id}/courses/{subject_name}"
        r = requests.get(url)

        return r
