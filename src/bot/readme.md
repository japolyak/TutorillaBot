## Environment variables

Environment variables:
* `APP_PORT` - port for the local development server with webhook. **Required** for `production`.
* `API_LINK` - link to the API. **Required** for `production`.
* `TIMEOUT` - request timeout to the API. **Required** for `production`.
* `IS_DEVELOPMENT` - determines development or production environment - `True` or `False`. **Required** for `development`.

Telegram related variables:

* `BOT_TOKEN` - bot token. **Required** for `development` and `production`.
* `WEB_APP_LINK` - link to the web app. **Required** for `development` and `production`.
* `WEBHOOK_URL` - webhook url - url of deployed `BOT` app. **Required** for `production`.

Redis related variables - all **required** for `production`:
* `REDIS_USERNAME` - redis username
* `REDIS_PASSWORD` - redis user password
* `REDIS_DB` - redis db number
* `REDIS_HOST` - redis host

## Handlers

### Message handler

There is one main message handler. Because of custom `i18n` implementation, it's necessary to complete `commands.py` file.

Each class that represents a users context should be inherited from `IContextBase` class.
