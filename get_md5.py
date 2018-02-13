from collections import Counter
import sqlite3
import json

db_path = '/media/gio/secondary/data/malwords/db/panda.db'
table_name = 'samples'
column1 = 'uuid'
column2 = 'filename'
column3 = 'md5'


conn = sqlite3.connect(db_path)
c = conn.cursor()

md5s = Counter()
md5_uuid_dict = {}

c.execute('SELECT {col1},{col2} FROM {tn}'.format(tn=table_name, col1=column1, col2=column3))
all_rows = c.fetchall()
for row in all_rows:
    md5s[row[1]] += 1
    md5_uuid_dict[row[1]] = row[0]

conn.close()

# Remove collisions
for md5 in md5s:
    if md5s[md5] > 1:
        md5_uuid_dict.pop(md5, None)

uuid_md5_dict = {value: key for key, value in md5_uuid_dict.items()}

json.dump(uuid_md5_dict, open('uuid_md5_map.json', 'w'), indent=2)
