#!/bin/sh

docker-compose up -d --build
sleep 5
docker exec mw-api "node" "server/connection.js"
sleep 5
docker exec mw-api "node" "server/load_data.js"
sleep 5
docker-compose logs -f api
