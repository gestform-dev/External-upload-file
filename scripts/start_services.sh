#!/usr/bin/env bash

docker run -p 5432:5432 -e POSTGRES_PASSWORD=password -v paperless_pgdata:/var/lib/postgresql/data -d postgres:13
docker run -d -p 6379:6379 redis:latest
docker run -p 3000:3000 -d gotenberg/gotenberg:7.8 gotenberg --chromium-disable-javascript=true --chromium-allow-list="file:///tmp/.*"
docker run -p 9998:9998 -d ghcr.io/paperless-ngx/tika:latest


# local test
sudo docker run --name db -p 5432:5432 -e POSTGRES_DB=paperless -e POSTGRES_USER=paperless -e POSTGRES_PASSWORD=paperless -v paperless_pgdata:/var/lib/postgresql/data -d postgres:13
sudo docker run --name redis -d -p 6379:6379 redis:latest
sudo docker run -p 8000:8000 --name paperless \
--link db:db \
--link redis:redis \
-e PAPERLESS_DEBUG='true' \
-e COMPOSE_PROJECT_NAME='paperless' \
-e PAPERLESS_TRUSTED_PROXIES='' \
-e PAPERLESS_REDIS='redis://redis:6379' \
-e PAPERLESS_DBHOST='db' \
-e PAPERLESS_DBPORT='5432' \
-e PAPERLESS_DBNAME='paperless' \
-e PAPERLESS_DBUSER='paperless' \
-e PAPERLESS_DBPASS='paperless' \
-e PAPERLESS_SECRET_KEY=
-e PAPERLESS_CORS_ALLOWED_HOSTS='http://localhost:4200,http://localhost:8000' \
-e PAPERLESS_OCR_LANGUAGE='eng' \
-e PAPERLESS_OCR_LANGUAGES='eng' \
-e PAPERLESS_TIME_ZONE='Europe/Paris' \
-e HEIC_TO_JPEG_API_URL=
