from string import Template

en = {
    "Welcome": Template("Glad You are back, $name"),
    "selected_language": Template("Wonderful! English has been chosen"),
    "first_name": Template("First name"),
    "last_name": Template("Last name"),
    "email": Template("Email"),
    "ProvideYourEmail": Template("Provide your email"),
    "ChooseYourTimeZone": Template("Choose your time zone"),
    "remaining_info": Template("Fill in the remaining information about yourself"),
    "congratulations": Template("Congratulations, you have registered, now choose what you want to do!"),
    "UseOnlyLatinLetters": Template("Use only latin letters"),
    "ProvideYourFirstname": Template("Provide your first name"),
    "ProvideYourLastname": Template("Provide your last name"),
    "GreatWaitForConfirmationByAdmin": Template("Great! Wait for confirmation by Admin"),
    "OneMoreTime": Template("Try one more time"),
    "UseOnlyDigits": Template("Use only digits"),
    "SomethingWentWrong": Template("Something went wrong. Repeat registration process! Press /start"),
    "WelcomeOnBoard": Template("Welcome on board, You have successfully registered. Now You can choose what do You want to do!"),
}
