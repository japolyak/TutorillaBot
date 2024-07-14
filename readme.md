# TutorBot

This is main application of the [TutotillaBot](https://github.com/users/japolyak/projects/2/views/4) project.

## Telegram settings

To be able to run the bot, you need to create a bot in `BotFather` in `Telegram` and get a token. After that it's necessary
to change the next settings in bot configuration:

* `/setprivacy` - change from ENABLED to DISABLED
* `/setinline` - enable inline queries

## Environment variables

In development, the app uses a `.env` file to store environment variables. The file should be located in the root directory of the project.
The app runs on Docker containers and uses Google Cloud Platform for reliability and scalability.
It requires the following environment variables for service configuration:

Environment variables:
* `APP_PORT` - port for the local development server with webhook
* `API_LINK` - link to the API
* `IS_DEVELOPMENT` - determines development or production environment - `True` or `False`. Not required in production.

Telegram related variables:

* `BOT_TOKEN` - bot token
* `WEB_APP_LINK` - link to the web app
* `USE_WEBHOOK` - use webhook or polling - `True` or `False` values. Not required in production.
* `WEBHOOK_URL` - webhook url

Redis related variables:
* `REDIS_USERNAME` - redis username
* `REDIS_PASSWORD` - redis user password
* `REDIS_DB` - redis db number
* `REDIS_HOST` - redis host

## Code style

* `PascalCase` - Classes, Enum and `i18n` dictionaries keys
* `snake_case` - functions, methods, variables, and arguments

## i18n

For each new language it's necessary to:
* add a new file in `i18n` folder.
* update `i18n.py` file.
* update all guards in `keyboard_button_guards.py` folder.

## Handlers

### Message handler

There is one main message handler. Because of custom `i18n` implementation, it's necessary to complete `commands.py` file.

Each class that represents a users context should be inherited from `IContextBase` class.
