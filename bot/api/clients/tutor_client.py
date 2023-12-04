import requests
from bot.config import api_link


class TutorClient:
    @staticmethod
    def available_subjects_tutor(user_id: int):
        url = f"{api_link}/tutor/{user_id}/available-course/"
        r = requests.get(url)

        return r

    @staticmethod
    def my_courses(user_id: int):
        url = f"{api_link}/tutor/{user_id}/course/"
        r = requests.get(url)

        return r

    @staticmethod
    def private_courses(user_id: int, subject_name: str):
        url = f"{api_link}/tutor/{user_id}/private-course/{subject_name}/"
        r = requests.get(url)

        return r

    @staticmethod
    def add_course(user_id: int, subject_id: int):
        url = f"{api_link}/tutor/{user_id}/course/{subject_id}/"
        r = requests.post(url)

        return r
