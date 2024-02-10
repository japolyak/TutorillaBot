import requests
from bot.config import api_link


class TutorClient:
    @staticmethod
    def available_subjects_tutor(user_id: int):
        url = f"{api_link}/tutors/{user_id}/available-courses/"
        r = requests.get(url)

        return r

    @staticmethod
    def add_course(user_id: int, subject_id: int):
        url = f"{api_link}/tutors/{user_id}/courses/{subject_id}/"
        r = requests.post(url)

        return r

    @staticmethod
    def get_private_course(user_id: int, private_course_id: int):
        url = f"{api_link}/tutors/{user_id}/private-course/{private_course_id}/"
        r = requests.get(url)

        return r
