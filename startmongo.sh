!#/bin/bash

docker run -d -p 27017:27017 -p 28017:28017 --name mongodb -v /home/ubuntu/composetest/db:/data/db -v /home/ubuntu/data:/data/jsons:ro mongo


docker exec -it mongodb mongo admin

db.createUser({ user: 'dbadmin', pwd: '', roles: [ { role: "userAdminAnyDatabase", db: "admin" } ] });

