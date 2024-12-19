from string import Template
from typing import Optional

from src.core.redis_configuration import redis_instance as r

from .locales.en_US import en


locales = {
    'en-US': en
}


def t(chat_id: int, key: str, locale: Optional[str] = None, **kwargs) -> str:
    if not locale:
        locale = r.hget(chat_id, 'locale') or 'en-US'

    phrase: Template = locales[locale][key]

    return phrase.substitute(**kwargs) if kwargs else phrase.template
