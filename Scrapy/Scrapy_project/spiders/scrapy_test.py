import json
import os

path = os.getcwd()
file_path = os.path.join(path, 'spiders\\fetch file\\cofact_getLink.json')

with open(file_path, encoding='utf-8') as fp:
    data = json.load(fp)

for i in data[1:10]:
    print(i['link'])