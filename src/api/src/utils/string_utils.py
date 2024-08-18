import json
import traceback
from traceback import FrameSummary
from typing import AnyStr
from urllib.parse import parse_qs


class StringUtils:
    @staticmethod
    def get_prop_as_int(qs: AnyStr, key: str, key2) -> int:
        parsed_query = parse_qs(qs)
        parsed_prop = json.loads(parsed_query.get(key, [''])[0])

        return parsed_prop[key2]

    @classmethod
    def create_error_message(cls, exc: Exception) -> str:
        exception_details = str(exc)
        exception_type = type(exc).__name__
        summary = list(filter(cls.__test, traceback.extract_tb(exc.__traceback__)))[-1]

        message_parts = (
            f"*{exception_type}* occurred in:",
            f">file: {cls.__replace_characters_in_telegram_rule(summary.filename)}",
            f">function: *{cls.__replace_characters_in_telegram_rule(summary.name)}*",
            f">line: {cls.__replace_characters_in_telegram_rule(summary.line)}",
            f">line number: {summary.lineno}",
            "Details:",
            f">{cls.__replace_characters_in_telegram_rule(exception_details)}"
        )

        message = "\n".join(message_parts)

        return message

    # https://stackoverflow.com/questions/3411771/best-way-to-replace-multiple-characters-in-a-string
    @staticmethod
    def __replace_characters_in_telegram_rule(text):
        for ch in ['_', '*', '[', ']', '(', ')', '~', '`', '>', '#', '+', '-', '=', '|', '{', '}', '.', '!']:
            if ch in text:
                text = text.replace(ch, "\\" + ch)

        return text

    @staticmethod
    def __test(summary: FrameSummary):
        return '.venv' not in summary.filename
