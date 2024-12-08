## Telegram settings

To be able to run the bot, you need to create a bot in `BotFather` in `Telegram` and get a token. After that it's necessary
to change the next settings in bot configuration:

* `/setprivacy` - change from ENABLED to DISABLED
* `/setinline` - enable inline queries

## Authentication and Authorization



## Code style

* `PascalCase` - Classes, Enum and `i18n` dictionaries keys
* `snake_case` - functions, methods, variables, and arguments

## Internalization

For each new language it's necessary to:
* add a new file in `i18n` folder.
* update `i18n.py` file.
* update all guards in `keyboard_button_guards.py` folder.