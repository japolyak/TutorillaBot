# TutorillaAPI

This API connects `BOT` and `Telegram WebApp` applications with database.

It's built using `FastAPI` for creating endpoints, `Pydantic` for data validation and settings management, and `SQLAlchemy` for ORM  and database operations.

## Database

The application uses a `PostgreSQL` database.

## Environment variables

In development, the app uses a `.env` file to store environment variables. The file should be located in the root directory of the project.
In production app runs on Docker containers and uses Google Cloud Platform for reliability and scalability.
Application requires the following environment variables for service configuration:

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
