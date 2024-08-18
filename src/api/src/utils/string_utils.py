import json
from typing import AnyStr
from urllib.parse import parse_qs


class StringUtils:
    @staticmethod
    def get_prop_as_int(qs: AnyStr, key: str, key2) -> int:
        parsed_query = parse_qs(qs)
        parsed_prop = json.loads(parsed_query.get(key, [''])[0])

        return parsed_prop[key2]
