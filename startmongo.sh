#!/bin/bash

# docker run -d -p 27017:27017 -p 28017:28017 --name mongodb -v /home/ubuntu/db:/data/db -v /home/ubuntu/data:/data/jsons:ro mongo --auth

echo "Starting Docker container"

docker run -it \
    -e MONGODB_ADMIN_USER=admin \
    -e MONGODB_ADMIN_PASS= \
    -e MONGODB_APPLICATION_DATABASE=mytestdatabase \
    -e MONGODB_APPLICATION_USER=testuser \
    -e MONGODB_APPLICATION_PASS=testpass \
    -p 27017:27017 \
    -p 28017:28017 \
    -v /home/ubuntu/db:/data/db \
    -v /home/ubuntu/data:/data/jsons:ro \
    --name mongodb mymongo
