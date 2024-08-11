#!/bin/sh

ROOT_DIR=/app

for file in $ROOT_DIR/assets/*.js $ROOT_DIR/index.html;
do
  sed -i 's|VITE_APP_API_URL_PLACEHOLDER|'${VITE_APP_API_URL}'|g' $file
  sed -i 's|VITE_APP_IS_DEV_PLACEHOLDER|'${VITE_APP_IS_DEV}'|g' $file
done

sed -i 's|listen       PORT;|listen       '${PORT}';|g' /etc/nginx/nginx.conf

exec "$@"
