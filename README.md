# TutorBot

Before running Bot it's necessary to change the next features in `BotFather` in `Telegram`:

* `/setprivacy` - change from ENABLED to DISABLED
* `/setinline` - enable inline queries

## Code style

For Classes, Enum and `i18n` dictionaries keys used `PascalCase`.

For functions, methods, variables, and arguments used `snake_case`.

## i18n

For each new language it's necessary to:
* add a new file in `i18n` folder.
* update `i18n.py` file.
* update all guards in `keyboard_button_guards.py` folder.

## Handlers

### Message handler

There is one main message handler. Because of custom `i18n` implementation, it's necessary to complete `commands.py` file.

Each class that represents a users context should be inherited from `IContextBase` class.

### Callback Query handler

[//]: # (TODO)

### Inline Handler

[//]: # (TODO)
