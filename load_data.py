from elasticsearch import Elasticsearch, helpers
import subprocess
import json
import os

index_name = 'malwords'
type_name = 'samples'
port_num = 9200
host = 'localhost'
data_dir = 'malwords'
analysis_dir = 'analysis'
raw_dir = 'raw'
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
    "content": {
        "type": 'text',
        "analyzer": "standard"
    },
    "raw": {
        "type": 'text',
        "analyzer": "standard"
    },
    "syscalls": {
        "type": "text",
        "analyzer": "simple"
    },
   "registry": {
        "type": "text",
        "analyzer": "simple"
    },
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

    analysis_files = set([i.split('.')[0] for i in os.listdir(analysis_dir)])
    print('Found {} analysis files.'.format(len(analysis_files)))

    raw_files = set([i.split('_')[0] for i in os.listdir(raw_dir)])
    print('Found {} raw files.'.format(len(raw_files)))

    # Set insert-friendly settings
    es.indices.put_settings(
        index=index_name,
        body={
            "refresh_interval" : "-1"
        }
    )
    
    # Perform bulk insert
    bulk_insert(
        es, 
        family_names,
        dir_files,
        md5_map,
        analysis_files,
        raw_files
    )

    # Set search-friendly settings
    es.indices.put_settings(
        index=index_name,
        body={
            "refresh_interval" : "1s"
        }
    )
 

def gen_data(dir_files, family_names, md5_map, analysis_files, raw_files):
    # Scan through the files
    for file_path in dir_files:
        # Obtain the words dictionary
        words = json.load(open(file_path, 'r'), encoding='utf-8')
        words = ' '.join(list(words.keys()))

        # Initialize variables
        syscalls = ''
        registry = ''
        raw = ''

        # Obtain the family label
        uuid = os.path.split(file_path)[1]

        # Check available data
        if uuid not in family_names:
            print('Missing family name:', uuid)
            continue
        if uuid not in md5_map:
            print('Missing md5:', uuid)
            continue

        if uuid in analysis_files:
            analysis = json.load(
                open(os.path.join(analysis_dir, uuid + '.json'), 'r')
            )

            syscalls = set()
            registry = set()

            for process, prc_dict in analysis.get('corrupted_processes', {}).items():
                syscalls |= set(prc_dict.get('system_calls', {}).keys())
                registry |= set(prc_dict.get('registry_activity', {}).keys())

            syscalls = ' '.join(syscalls)
            registry = ' '.join(registry)
        else:
            print('missing analysis:', uuid)

        if uuid in raw_files:
            raw_file = os.path.join(raw_dir, uuid + '_ss.txt.gz')
            proc = subprocess.Popen(
                ['gzip', '-cdfq', raw_file], stdout=subprocess.PIPE, bufsize=4096
            )
            raw = set()
            
            lines = proc.stdout
            for line in lines:
                line = line.strip().split()
                raw.add(line[0].decode('utf-8'))

            raw = ' '.join(raw)
        else:
            print('missing raw:', uuid)


        label = family_names[uuid]
        md5_hash = md5_map[uuid]

        # Prepare dictionary
        source_dict = {
            "family": label,
            "content": words,
            "md5": md5_hash,
            "syscalls": syscalls,
            "registry": registry,
            "raw": raw
        }

        yield {
            '_op_type': 'index',
            '_index': index_name,
            '_type': type_name,
            '_id': uuid,
            '_source': source_dict
        }


def bulk_insert(es, family_names, dir_files, md5_map, analysis_files, raw_files):
    for success, info in helpers.parallel_bulk(   
        es,
        gen_data(dir_files, family_names, md5_map, analysis_files, raw_files),
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
