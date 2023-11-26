from .locales.en_EN import en
from .locales.pl_PL import pl
from .locales.ru_RU import ru
from .locales.ua_UA import ua
from string import Template

langs = {
    'ua': ua,
    'ru': ru,
    'pl': pl,
    'en': en
}


def t(lang: str, key: str, **kwargs) -> str:
    phrase: Template = langs[lang][key]

    return phrase.substitute(**kwargs) if kwargs else phrase.template
