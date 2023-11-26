import requests
import logging
from ..config import api_link


class SessionApi:
    base_url = 'session/'

    @staticmethod
    def get_session(tg_id: int) -> dict:
        url = f"{api_link}{SessionApi.base_url}{tg_id}/"

        try:
            response = requests.get(url)
            response.raise_for_status()

            data = response.json()
            return data
        except requests.RequestException as e:
            logging.error(e)
            return {}

    @staticmethod
    def set_session(session: dict):
        url = f"{api_link}{SessionApi.base_url}"

        response = requests.post(url, json=session)
        response.raise_for_status()

        return response
