#!/bin/sh

docker-compose up -d --build
sleep 10
python 'load_data.py'
sleep 10
docker-compose logs -f api
