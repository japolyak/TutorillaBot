from string import Template
from .locales.en_EN import en
from .locales.pl_PL import pl
from .locales.ru_RU import ru
from .locales.ua_UA import ua
from bot.redis.redis_client import r

langs = {
    # 'ua-UA': ua,
    # 'ru-RU': ru,
    # 'pl-PL': pl,
    'en-US': en
}


def t(tg_id: int, key: str, locale: str | None = None, **kwargs) -> str:
    if not locale:
        locale = r.hget(tg_id, 'locale') or 'en-US'

    phrase: Template = langs[locale][key]

    return phrase.substitute(**kwargs) if kwargs else phrase.template
