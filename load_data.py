from elasticsearch import Elasticsearch, helpers
import json
import os

index_name = 'malwords'
type_name = 'samples'
port_num = 9200
host = 'localhost'
data_dir = 'malwords'
labels_file = 'labels.json'
md5_file = 'uuid_md5_map.json'

conn_conf = {
    'host': host,
    'port': port_num,
    'timeout': 3600
}

index_settings = {
    "index.mapping.total_fields.limit": 500000,
    "number_of_shards" : 1, 
    "number_of_replicas" : 0,
    "index.codec": "best_compression"
} 

mapping_schema = {
    "content": {"type": 'nested' },
    "family": {"type": 'keyword'},
    "md5": {"type": 'keyword'}
}


def create_connection():
    # Initiate connection
    es = Elasticsearch([conn_conf,], timeout=600)

    # Create Index
    es.indices.create(index=index_name, body=index_settings, ignore=400)

    # Create mapping
    es.indices.put_mapping(
        index=index_name, 
        doc_type=type_name, 
        body={"properties": mapping_schema}
    )

    return es


def load_data(es):
    # Read labels file and the md5 mapping
    family_names = json.load(open(labels_file, 'r'), encoding='utf-u')
    md5_map = json.load(open(md5_file, 'r'), encoding='utf-u')

    # Scan the data directory
    dir_files = [os.path.join(data_dir, i) for i in os.listdir(data_dir)]
    print('Found {} files to index.'.format(len(dir_files)))

    # Set insert-friendly settings
    es.indices.put_settings(
        index=index_name,
        body={
            "refresh_interval" : "-1"
        }
    )
    
    # Perform bulk insert
    bulk_insert(es, family_names, dir_files, md5_map)

    # Set search-friendly settings
    es.indices.put_settings(
        index=index_name,
        body={
            "refresh_interval" : "1s"
        }
    )
 

def gen_data(dir_files, family_names, md5_map):
    # Scan through the files
    for file_path in dir_files:
        # Obtain the words dictionary
        words = json.load(open(file_path, 'r'), encoding='utf-8')

        # Obtain the family label
        uuid = os.path.split(file_path)[1]
        if uuid not in family_names or uuid not in md5_map:
            print('Missing key:', uuid)
            continue
        label = family_names[uuid]
        md5_hash = md5_map[uuid]

        # Prepare dictionary
        source_dict = {
            "family": label,
            "content": words,
            "md5": md5_hash
        }

        yield {
            '_op_type': 'index',
            '_index': index_name,
            '_type': type_name,
            '_id': uuid,
            '_source': source_dict
        }


def bulk_insert(es, family_names, dir_files, md5_map):
    for success, info in helpers.parallel_bulk(   
        es,
        gen_data(dir_files, family_names, md5_map),
        chunk_size=10,
        thread_count=4,
        raise_on_exception=True,
        raise_on_error=True
    ):
        if not success:
            print('A document failed:', info)
            
    es.indices.refresh()
    print(es.count(index=index_name))


def main():
    es = create_connection()
    load_data(es)

if __name__ == "__main__":
    main()
