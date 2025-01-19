# Telegram setup

Tutorilla platform aims to use web application as it's main control panel.
Telegram requires web application to run under TSL, what is not development friendly.
Because of that telegram provides test environment, where web apps can be used under HTTP links without TLS.
To set up test environment follow next steps:

1. Follow [instruction](https://core.telegram.org/bots/webapps#using-bots-in-the-test-environment) to set up your test account.
1. Use [debug instruction](https://core.telegram.org/bots/webapps#debug-mode-for-mini-apps) to set up telegram debugging environment based on your preferences.
1. Using test account open chat with `@botfather`, create bot and get it's token.
1. Using `@botfather` enable `/setprivacy` and `/setinline` in bot configuration.

After all steps are done you can move to development.

# Development

## Project run

All you need to run projects is to:

1. Install Python in 3.12 version
1. Install npm
1. Place in `src` directory `.env` file with the following structure:
    ```
    IS_DEVELOPMENT=1
    
    BOT_TOKEN=your_test_tg_bot_token
    ADMIN_TG_ID=your_tg_admin_id
    WEB_APP_LINK=http://127.0.0.1:5173
    
    DB_USER=postgres
    DB_PASSWORD=postgres
    ```

## Applications run

[//]: # (TODO)

## Classic web app development

[//]: # (TODO)

## Code style

Python code style:

* `PascalCase` - Classes, Enum and `i18n` dictionaries keys
* `snake_case` - functions, methods, variables, and arguments

TypeScript code style:

* `PascalCase` - Classes and `i18n` json keys
* `camelCase` - functions, methods, variables, and props

## Internalization

For each new language it's necessary to:
* add a new file in `i18n` folder.
* update `i18n.py` file.
* update all guards in `keyboard_button_guards.py` folder.

# Testing

After all features and bugs were fixed it essential to run all 3 apps using docker and check all changes.

To start testing we need to:

1. Add to `.env` file (or uncomment) next rows:
    ```
    DB_HOST=postgres
    
    API_PORT=8000
    API_LINK=http://tutorilla-api:8000
    
    REDIS_HOST=redis
    
    WEB_APP_PORT=5173
    VITE_APP_API_LINK=http://localhost:8000
    ```
1. After that using command line switch to `src` directory of the project and run
    ```shell
    docker compose -f docker-compose-dev.yaml -p tutorilla up -d
    ```

Once all 2 steps above are done and all 3 containers are running you can start manual testing process.

# Version releasing

Mother of branches is `main`.
It's used for versioning, image building and deploying to server.

All changes which were done on side branches should be later merged to `development` branch.
When version has to be released, `development` branch should be merged to `main` branch.

Each push to remote `main` branch should be followed by tag in accordance with semantic versioning - `vX.Y.Z`
