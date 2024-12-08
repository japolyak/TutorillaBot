## Environment variables

Environment variables:
* `ALLOWED_ORIGINS` - list of divided by `&` allowed origins for CORS. **Required** for `production`
* `IS_DEVELOPMENT` - determines development or production environment - `True` or `False`. **Required** for `development`.
* `ALGORITHM` - algorithm used for encoding token. **Required**
* `ACCESS_TOKEN_EXPIRE_MINUTES` - token's expiration time in minutes. **Required** for `production`

Telegram related variables:

* `BOT_TOKEN` - bot token. **Required** for `development` and `production`.
* `ADMIN_TG_ID` - bot admin telegram id. In `development` it's also a developer user. **Required** for `development` and `production`.

Database related variables - all are **required** for `production`:
* `DB_USER` - db user
* `DB_PASSWORD` - db password
* `DB_NAME` - db name
