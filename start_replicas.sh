#!/bin/sh

docker run -p 37017:27017 -v /home/gio/projects/malwords_search/keyfile:/home/mongodb/keyfile --name mongo-local-001 --net mongo-rs-local -d mongo:3.4 --auth --replSet rslocal01 --keyFile /home/mongodb/keyfile

docker run -p 37018:27017 -v /home/gio/projects/malwords_search/keyfile:/home/mongodb/keyfile --name mongo-local-002 --net mongo-rs-local -d mongo:3.4 --auth --replSet rslocal01 --keyFile /home/mongodb/keyfile

docker run -p 37019:27017 -v /home/gio/projects/malwords_search/keyfile:/home/mongodb/keyfile --name mongo-local-003 --net mongo-rs-local -d mongo:3.4 --auth --replSet rslocal01 --keyFile /home/mongodb/keyfile

docker run -d -p 9200:9200 -p 9300:9300 -e ES_JAVA_OPTS="-Xms8g -Xmx8g" --name=elasticsearch1 elasticsearch

docker exec -it mongo-local-001 mongo

