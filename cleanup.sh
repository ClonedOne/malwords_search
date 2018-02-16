#!/bin/sh

docker stop mw-api mw-frontend mw-search
docker mw-api mw-frontend mw-search
docker volume rm malwordssearch_esdata
