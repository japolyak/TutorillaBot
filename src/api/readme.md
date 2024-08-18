# TutorillaAPI

This API connects `BOT` and `Telegram WebApp` applications with database.

It's built using `FastAPI` for creating endpoints, `Pydantic` for data validation and settings management, and `SQLAlchemy` for ORM  and database operations.

## Database

The application uses a `PostgreSQL` database hosted on a `Google Cloud` virtual machine located in the North America region.
This choice was based on financial considerations. Due to the database's location, requests to the database may take slightly longer than usual.
To mitigate this, some requests are made (and others will be rewritten) as transactions and functions to reduce the number of database requests.

## Environment variables

In development, the app uses a `.env` file to store environment variables. The file should be located in the root directory of the project.
In production app runs on Docker containers and uses Google Cloud Platform for reliability and scalability.
Application requires the following environment variables for service configuration:

Environment variables:
* `ALLOWED_ORIGINS` - list of divided by `&` allowed origins for CORS. **Required** for `production`
* `IS_DEVELOPMENT` - determines development or production environment - `True` or `False`. **Required** for `development`.

Telegram related variables:

* `BOT_TOKEN` - bot token. **Required** for `development` and `production`.
* `ADMIN_TG_ID` - bot admin telegram id. In `development` it's also a developer user. **Required** for `development` and `production`.

Database related variables - all are **required** for `production`:
* `DB_USER` - db user
* `DB_PASSWORD` - db password
* `DB_HOST` - db host
* `DB_NAME` - db name
* `DB_PORT` - db port
