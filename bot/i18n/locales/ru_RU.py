from string import Template

ru = {
    "welcome": Template("Добро пожаловать, $name"),
    "selected_language": Template("Замечательно! Выбран русский"),
    "first_name": Template("Имя"),
    "last_name": Template("Фамилия"),
    "phone": Template("Телефон"),
    "email": Template("E-mail"),
    "enter_first_name": Template("Введите имя"),
    "enter_last_name": Template("Введите фамилию"),
    "enter_phone": Template("Введите номер телефона"),
    "enter_email": Template("Введите электронную почту"),
    "phone_added": Template("Номер телефона добавлен"),
    "remaining_info": Template("Заполните оставшуюся информацию о себе"),
    "congratulations": Template("Поздравляем, вы зарегистрированы, а теперь выберите, что вы хотите делать!"),
}
