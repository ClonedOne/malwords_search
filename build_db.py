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
    username=username,
    password=password,
)

db = client['samples']
words = db.words

for json_file in os.listdir(data_path):
    sample_words = json.load(open(os.path.join(data_path, json_file), 'r'))
    sample_words['_id'] = json_file.split('.')[0].strip()
    words_id = words.insert_one(sample_words)
    print(words_id, words['_id'])



