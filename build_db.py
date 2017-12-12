import urllib.parse
import pymongo
import sys



if len(sys.argv < 2):
    print('Please specify data folder, user name, and password')
    exit(1)

data_path = sys.argv[1]
username = urllib.parse.quote_plus(sys.argv[2])
password = urllib.parse.quote_plus(sys.argv[3])
client = MongoClient(
    username=username,
    password=password,
)



