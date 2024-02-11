from string import Template

pl = {
    "welcome": Template("Witamy, $name"),
    "selected_language": Template("Wspaniale! Wybrano polski"),
    "first_name": Template("Imię"),
    "last_name": Template("Nazwisko"),
    "phone": Template("Telefon"),
    "email": Template("E-mail"),
    "enter_first_name": Template("Wprowadź imię"),
    "enter_last_name": Template("Wprowadź nazwisko"),
    "enter_phone": Template("Wprowadź numer telefonu"),
    "enter_email": Template("Wprowadź adres e-mail"),
    "phone_added": Template("Numer telefonu dodany"),
    "remaining_info": Template("Wypełnij pozostałe informacje o sobie"),
    "congratulations": Template("Gratulacje, zarejestrowałeś się a teraz wybierz, co chcesz zrobić!"),
}
