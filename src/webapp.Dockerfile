FROM node:20 as build-stage

WORKDIR /app

COPY web_app/package*.json ./
RUN npm install

COPY web_app/ .
ARG VERSION
ENV VITE_APP_VERSION=${VERSION}
RUN npm run build

FROM nginx:1.25.3 as production-stage
RUN mkdir /app

COPY --from=build-stage /app/dist /app
COPY web_app/nginx.conf /etc/nginx/nginx.conf

COPY web_app/substitute_environment_variables.sh /docker-entrypoint.d/

RUN chmod +x /docker-entrypoint.d/substitute_environment_variables.sh
