## Deployment

Structure of production version of `.env` file

```
IS_DEVELOPMENT=0

DB_USER=your_db_user
DB_PASSWORD=your_db_password
DB_NAME=your_db_name
DB_PORT=your_db_port
DB_HOST=postgres

#API
ALLOWED_ORIGINS=allowed_origins_separated_by_&_char
API_PORT=your_api_port
ALGORITHM=your_encryption_algorithm
API_LINK=http://api_container_name:API_PORT

#Telegram
BOT_TOKEN=your_tg_bot_token
ADMIN_TG_ID=your_tg_admin_id
WEB_APP_LINK=your_web_app_link

#Redis
REDIS_HOST=redis

#WebApp
WEB_APP_PORT=your_web_app_port
VITE_APP_API_LINK=https://your.domain.com/api
```

```shell
docker network create tutorilla-network

docker compose -f docker-compose-storages.yaml -p tutorilla up -d
```