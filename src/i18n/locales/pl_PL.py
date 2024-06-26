from string import Template

pl = {
    "welcome": Template("Witamy, $name"),
    "selected_language": Template("Wspaniale! Wybrano polski"),
    "first_name": Template("Imię"),
    "last_name": Template("Nazwisko"),
    "email": Template("E-mail"),
    "enter_first_name": Template("Wprowadź imię"),
    "enter_last_name": Template("Wprowadź nazwisko"),
    "enter_email": Template("Wprowadź adres e-mail"),
    "remaining_info": Template("Wypełnij pozostałe informacje o sobie"),
    "congratulations": Template("Gratulacje, zarejestrowałeś się a teraz wybierz, co chcesz zrobić!"),
}
