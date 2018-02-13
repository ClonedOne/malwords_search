#!/bin/sh

curl -XPUT 'localhost:9200/malwords/_settings' -d ' {
    "index" : {
    	"refresh_interval" : "-1",
        "number_of_replicas" : 0
    }
}'