!#/bin/bash

docker run -d -p 27017:27017 -p 28017:28017 --name mongodb -v /home/ubuntu/composetest/data/small:/data/db:ro mongo
