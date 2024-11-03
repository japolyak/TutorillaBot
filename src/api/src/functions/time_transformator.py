from datetime import datetime


def transform_class_time(date_in_unix_ts: int, timezone: float) -> str:
    date_in_unix_ts /= 1000

    if timezone != 0:
        date_in_unix_ts += timezone * 60 *60

    return datetime.fromtimestamp(date_in_unix_ts).strftime('%H:%M %d-%m-%Y')
