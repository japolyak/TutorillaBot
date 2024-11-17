from hashlib import sha256
from hmac import new as hmac_new
from urllib.parse import unquote

from src.common.config import bot_token


def init_data_is_valid(init_data: str, c_str = "WebAppData") -> bool:
    # Reimplemented based on https://gist.github.com/nukdokplex/79438159cb4e757c15ded719e1a83163
    hash_string = ""

    init_data_dict = dict()

    for chunk in init_data.split("&"):
        [key, value] = chunk.split("=", 1)
        if key == "hash":
            hash_string = value
            continue
        init_data_dict[key] = unquote(value)

    if hash_string == "":
        return False

    init_data = "\n".join(
        [
            f"{key}={init_data_dict[key]}"
            for key in sorted(init_data_dict.keys())
        ]
    )

    secret_key = hmac_new(c_str.encode(), bot_token.encode(), sha256).digest()
    computed_hash = hmac_new(secret_key, init_data.encode(), sha256).hexdigest()

    return computed_hash == hash_string
