from string import Template
from src.i18n.locales.en_US import en
from src.redis_service.redis_client import r


locales = {
    'en-US': en
}


def t(chat_id: int, key: str, locale: str | None = None, **kwargs) -> str:
    if not locale:
        print('locale was not provided')
        locale = r.hget(chat_id, 'locale') or 'en-US'

    phrase: Template = locales[locale][key]

    return phrase.substitute(**kwargs) if kwargs else phrase.template
