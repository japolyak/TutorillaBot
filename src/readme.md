

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

docker-compose -f docker-compose-storages.yml up -d

docker-compose -f docker-compose-apps.yml up -d
```