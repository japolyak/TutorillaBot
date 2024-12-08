# Server configuration

This document describes the configuration steps for running the Tutorilla platform on a Debian 12 Hetzner Cloud server
using a Duck DNS domain, secured by Let’s Encrypt SSL, served by Nginx as a reverse proxy, and optionally using Redis.

## DNS

Telegram requires that WebApps integrated via its Bot API must be served over `HTTPS`.
If you do not have a permanent domain or static IP, Duck DNS provides a free and convenient way to obtain a domain name
that dynamically maps to your server’s IP address.

## Docker Configuration

### Docker

```shell
```

## SSL configuration

### Certbot and Nginx Plugin

Installs `certbot` for SSL certificate management and the `python3-certbot-nginx` plugin to automate `Nginx` configuration tasks.

```shell
sudo apt update
sudo apt install nginx
sudo apt install certbot python3-certbot-nginx
```

### Obtain and check a Certificate

Generates and installs an SSL certificate for `your.domain.com`.

```shell
sudo certbot --nginx -d your.domain.com
sudo certbot certificates # certificate check
```

### Automatic Renewal

Schedules automatic certificate renewal and reloads Nginx daily ar 1 AM

```shell
sudo crontab -e

0 1 * * * sudo certbot renew --quiet && sudo systemctl reload nginx

sudo nginx -t

sudo systemctl reload nginx # or restart
```

## Nginx Configuration

### Location of Config Files:

The primary Nginx configuration file for your domain will be located in `/etc/nginx/sites-available/mydomain`.
Within this directory, you will have a file named `default` (or a file named after your domain) that controls how incoming traffic is handled.

### Sample `default` File Configuration:
```shell
server {
    listen [::]:443 ssl ipv6only=on; # managed by Certbot
    listen 443 ssl; # managed by Certbot
    server_name your.domain.com;

    ssl_certificate /etc/letsencrypt/live/your.domain.com/fullchain.p>
    ssl_certificate_key /etc/letsencrypt/live/your.domain.com/privkey>
    include /etc/letsencrypt/options-ssl-nginx.conf; # managed by Certbot
    ssl_dhparam /etc/letsencrypt/ssl-dhparams.pem; # managed by Certbot

    location / {
            proxy_pass http://localhost:your_web_app_port; # replace with your web app port
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
    }

    location /api/ {
            proxy_pass http://localhost:your_api_port; # replace with your api port
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
            
            rewrite ^/api/(.*)$ /$1 break;
    }
}
```

* `server_name your.domain.com` - specifies which domain this server block should respond to.
* `listen [::]:443 ssl ipv6only=on;` and `listen 443 ssl;` - configures the server to listen for secure HTTPS connections on both IPv4 and IPv6 addresses.
* SSL Certificate and Key Settings:
  * `ssl_certificate` and `ssl_certificate_key` point to the certificate and key files obtained by Certbot. 
  * The `include` and `ssl_dhparam` lines provide additional security parameters as recommended by Certbot.
* Reverse Proxy Sections (location blocks):
  * `location /` - Proxies all requests from the root path to the web application running on `http://localhost:your_web_app_port`.
  * `location /api/` - Proxies requests starting with /api to a different backend service running on `http://localhost:your_api_port`. The rewrite directive removes the `/api` prefix before forwarding the request, so the backend sees a clean path.

### Testing and Reloading Configuration

* Run `sudo nginx -t` to test for syntax errors.
* Run `sudo systemctl reload nginx` (or `restart`) to apply configuration changes.

## Redis setup

```shell
sudo apt update
sudo apt install redis-server -y
redis-server --version
```

Installs Redis and confirms its version.