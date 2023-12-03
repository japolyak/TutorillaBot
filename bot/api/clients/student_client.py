import requests
from bot.config import api_link


class StudentClient:
    @staticmethod
    def available_courses_student(user_id: int):
        url = f"{api_link}/student/{user_id}/available-course/"
        r = requests.get(url)

        return r

    @staticmethod
    def my_classes(user_id: int):
        url = f"{api_link}/student/{user_id}/course/"
        r = requests.get(url)

        return r

    @staticmethod
    def enroll_in_course(user_id: int, course_id: int):
        url = f"{api_link}/student/{user_id}/course/{course_id}/"
        r = requests.post(url)

        return r

    @staticmethod
    def private_courses(user_id: int, subject_name: str):
        url = f"{api_link}/student/{user_id}/private-course/{subject_name}"
        r = requests.get(url)

        return r

    @staticmethod
    def course_tutors(user_id: int, subject_name: str):
        url = f"{api_link}/student/{user_id}/course/{subject_name}"
        r = requests.get(url)

        return r
