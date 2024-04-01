from string import Template

ua = {
    "welcome": Template("Вітаємо, $name"),
    "selected_language": Template("Чудово! Обрано українську мову"),
    "first_name": Template("Ім'я"),
    "last_name": Template("Прізвище"),
    "email": Template("E-mail"),
    "enter_first_name": Template("Введіть ім'я"),
    "enter_last_name": Template("Введіть прізвище"),
    "enter_email": Template("Введіть електронну пошту"),
    "remaining_info": Template("Заповніть решту інформації про себе"),
    "congratulations": Template("Вітаємо, ви зареєструвалися а тепер виберіть, що ви хочете робити!"),
}
