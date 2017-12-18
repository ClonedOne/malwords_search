#!/bin/bash

echo "Starting Docker container"

mongoadminpwd=$(head -n 1 .adminpwd)
mongouserpwd=$(head -n 1 .userpwd)
echo $mongoadminpwd

docker run -it \
    -e MONGODB_ADMIN_USER=admin \
    -e MONGODB_ADMIN_PASS=$mongoadminpwd \
    -e MONGODB_APPLICATION_DATABASE=mytestdatabase \
    -e MONGODB_APPLICATION_USER=testuser \
    -e MONGODB_APPLICATION_PASS=$mongouserpwd \
    -p 27017:27017 \
    -p 28017:28017 \
    -v /home/gio/projects/malwords_search/db:/data/db \
    -v /media/gio/secondary/data/malwords/small:/data/jsons:ro \
    --name mongodb mymongo
