# Deployment

* Redis 7.4.1
* PostgreSQL 16.5-bookworm

## DNS

Used free dynamic Duck DNS - https://www.duckdns.org

## SSL setup

Used Linux (Debian 12)

```sh
sudo apt update

sudo apt install certbot python3-certbot-nginx

sudo certbot --nginx -d your.domain.com

sudo certbot certificates # certificate check

```

```sh
sudo crontab -e

0 1 * * * sudo certbot renew --quiet && sudo systemctl reload nginx

sudo nginx -t

sudo systemctl reload nginx # or restart
```

Change directory to `/etc/nginx/sites-available/mydomain`

and setup `default` file
```sh
server {
    listen [::]:443 ssl ipv6only=on; # managed by Certbot
    listen 443 ssl; # managed by Certbot
    server_name your.domain.com;

    ssl_certificate /etc/letsencrypt/live/your.domain.com/fullchain.p>
    ssl_certificate_key /etc/letsencrypt/live/your.domain.com/privkey>
    include /etc/letsencrypt/options-ssl-nginx.conf; # managed by Certbot
    ssl_dhparam /etc/letsencrypt/ssl-dhparams.pem; # managed by Certbot

    location / {
            proxy_pass http://localhost:3021;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
    }

    location /api/ {
            proxy_pass http://localhost:8000;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
            
            rewrite ^/api/(.*)$ /$1 break;
    }
}
```

## Deployment

Structure of development version of `.env` file

```
IS_DEVELOPMENT=0

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
WEB_APP_LINK=your_web_app_link

#Redis
REDIS_HOST=redis
REDIS_DB=your_redis_db
REDIS_PASSWORD=your_redis_password
REDIS_USERNAME=your_redis_username

#WebApp
WEB_APP_PORT=your_web_app_port
VITE_APP_API_LINK=https://your.domain.com/api
```
