import re


class Validator:
    @staticmethod
    def validate_name(name):
        return re.match("^[a-zA-Z]+$", name)

    @staticmethod
    def email_validator(email):
        regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'

        return re.fullmatch(regex, email)
