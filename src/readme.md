

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

move to `/etc/nginx/sites-available/mydomain`

and setup
```sh

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