# malwords_search

This repository contains some scirpts to setup a small search engine to provide text search capabilities over the [Malwords](https://github.com/ClonedOne/malwords) dataset.

The goal was to setup everything using docker containers for maximum portability.

To build up the service run:

```bash
source to_source.sh
openssl rand -base64 755 > keyfile  
chmod 400 keyfile
chown 999:999 keyfile
sh start_replicas.sh
# use the settings in connector_config.json (insert pwd)
sh configuration.sh
cd _site
http-server
```

The front end is built using [Calaca](https://github.com/romansanchez/Calaca) and served with [http-server](https://github.com/indexzero/http-server) using Node.js.
