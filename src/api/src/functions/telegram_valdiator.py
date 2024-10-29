import hashlib
import hmac
import os


def init_data_is_valid(parsed_init_data: dict) -> bool:
    bot_token = os.getenv("BOT_TOKEN")

    parsed_auth_date = parsed_init_data.get('auth_date', [''])[0]
    parsed_query_id = parsed_init_data.get('query_id', [''])[0]
    parsed_user = parsed_init_data.get('user', [''])[0]
    parsed_hash = parsed_init_data.get('hash', [''])[0]

    data_check_string = f"auth_date={parsed_auth_date}\nquery_id={parsed_query_id}\nuser={parsed_user}"

    secret_key = hmac.new("WebAppData".encode(), bot_token.encode(), hashlib.sha256).digest()
    computed_hash = hmac.new(secret_key, data_check_string.encode(), hashlib.sha256).digest()
    hex_signature = ''.join(format(b, '02x') for b in computed_hash)

    return hex_signature == parsed_hash
