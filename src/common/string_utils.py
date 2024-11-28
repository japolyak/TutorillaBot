import traceback
from traceback import FrameSummary


class StringUtils:
    @classmethod
    def is_none_or_empty(cls, val) -> bool:
        return True if val else False

    @classmethod
    def create_error_message(cls, exc: Exception) -> str:
        exception_details = str(exc)
        exception_type = type(exc).__name__
        files = list(filter(cls.__remove_venv_files, traceback.extract_tb(exc.__traceback__)))

        if files:
            summary = files[-1]

            message_parts = (
                f"*{exception_type}* occurred in:",
                f">file: {cls.__replace_characters_in_telegram_rule(summary.filename)}",
                f">function: *{cls.__replace_characters_in_telegram_rule(summary.name)}*",
                f">line: {cls.__replace_characters_in_telegram_rule(summary.line)}",
                f">line number: {summary.lineno}",
                "Details:",
                f">{cls.__replace_characters_in_telegram_rule(exception_details)}"
            )
        else:
            message_parts = (
                f"*{exception_type}* occurred\.",
                "Details:",
                f"{cls.__replace_characters_in_telegram_rule(exception_details)}"
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
    def __remove_venv_files(summary: FrameSummary):
        return '.venv' not in summary.filename
