## Deployment

Structure of development version of `.env` file

```
IS_DEVELOPMENT=1

DB_USER=your_db_user
DB_PASSWORD=your_db_password
DB_NAME=your_db_name
DB_PORT=your_db_port
DB_HOST=postgres

#API
ALLOWED_ORIGINS=allowed_origins_separated_by_&
API_PORT=your_api_port
ALGORITHM=your_encryption_algorithm
API_LINK=http://api_container_name:API_PORT

#Telegram
BOT_TOKEN=your_tg_bot_token
ADMIN_TG_ID=your_tg_admin_id
WEB_APP_LINK=any_https_link

#Redis
REDIS_HOST=redis
REDIS_DB=your_redis_db
REDIS_PASSWORD=your_redis_password
REDIS_USERNAME=your_redis_username

#WebApp
WEB_APP_PORT=your_web_app_port
VITE_APP_API_LINK=https://your.domain.com/api
```
