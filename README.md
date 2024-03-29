# TutorBot

Before running Bot it's necessary to change the next features in BotFather:

* `/setprivacy` - change from ENABLED to DISABLED
* `/setinline` - enable inline queries

## i18n

For each new language it's necessary to:
* add a new file in `i18n` folder.
* update `i18n.py` file.
* update all guards in `keyboard_button_guards.py` folder.

## Guards

For each new `KeyboardButton()` it's necessary to add a new guard regarding context in `keyboard_button_guards.py` folder.
