import urllib.parse
import pymongo
import json
import sys
import os



if len(sys.argv) < 4:
    print('Please specify data folder, user name, and password')
    exit(1)

data_path = sys.argv[1]
username = urllib.parse.quote_plus(sys.argv[2])
password = urllib.parse.quote_plus(sys.argv[3])

client = pymongo.MongoClient(
    host=['localhost:37017'],
    username=username,
    password=password,
)

db = client['samples']
words = db.words

json_files = sorted(os.listdir(data_path))
n_files = len(json_files)
i = 0

for json_file in json_files:
    sample_words = json.load(open(os.path.join(data_path, json_file), 'r'))
    to_append = {"words": []}

    for word, weight in sample_words.items():
        to_append["words"].append({"word":word, "weight":weight})    

    to_append['_id'] = json_file.split('.')[0].strip()
    words_id = words.insert_one(to_append)

    i += 1
    perc = (i / n_files) * 100 
    if perc % 10 == 0:
        print('Building DB: {}%'.format(perc))

