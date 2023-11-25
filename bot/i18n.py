from string import Template


def t(lang: str, key: str, **kwargs) -> str:
    phrase = langs[lang][key]

    return phrase.substitute(**kwargs) if kwargs else phrase


ua_Ua = {
    'welcome': Template('Вітаємо, $name'),
    'language_changed': Template('Мову змінено на $language')
}

ru_Ru = {
    'welcome': Template('Добро пожаловать, $name'),
    'language_changed': Template('Язык изменен на $language')
}

pl_Pl = {
    'welcome': Template('Witamy, $name'),
    'language_changed': Template('Język zmieniony na $language')
}

en_En = {
    'welcome': Template('Welcome, $name'),
    'language_changed': Template('Language changed to $language')
}

langs = {
    'ua': ua_Ua,
    'ru': ru_Ru,
    'pl': pl_Pl,
    'en': en_En
}
