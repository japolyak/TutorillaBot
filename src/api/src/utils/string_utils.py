from typing import AnyStr


class StringUtils:
    @classmethod
    def is_none_or_empty(cls, value: AnyStr) -> bool:
        if value is None:
            return True
        elif len(value) == 0:
            return True

        return False
