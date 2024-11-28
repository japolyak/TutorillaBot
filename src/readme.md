

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

```
docker network create tutorilla-network

docker compose -f docker-compose-storages.yml -p tutorilla up -d

docker compose -f docker-compose-apps.yml -p tutorilla up -d
```

## Redis setup

```sh
sudo apt update

sudo apt install redis-server -y

redis-server --version

#replace username, password and table_number (0-15)
ACL SETUSER username on >password +@all -select +select|table_number ~*
```