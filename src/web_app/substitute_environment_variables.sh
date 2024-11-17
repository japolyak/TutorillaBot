#!/bin/sh

ROOT_DIR=/app

for file in $ROOT_DIR/assets/*.js $ROOT_DIR/index.html;
do
  sed -i 's|VITE_APP_API_LINK_PLACEHOLDER|'${VITE_APP_API_LINK}'|g' $file
  sed -i 's|VITE_APP_IS_DEV_PLACEHOLDER|'${IS_DEVELOPMENT}'|g' $file
done

sed -i 's|listen       WEB_APP_PORT;|listen       '${WEB_APP_PORT}';|g' /etc/nginx/nginx.conf

exec "$@"
