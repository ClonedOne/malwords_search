#!/bin/sh

rootpwd=$(head -n 1 .rootpwd)

python build_db.py /media/gio/secondary/data/malwords/small root $rootpwd

curl -XPUT localhost:9200/samples/
curl -XPUT localhost:9200/samples/_settings -d '{"index.mapping.total_fields.limit": 500000}'

rm mongo-connector.log oplog.timestamp
mongo-connector -m localhost:37017 -t http://localhost:9200  -d elastic2_doc_manager -c connector_config.json -n samples.words --admin-username 'root' --password $rootpwd
