from pymongo import MongoClient
from pprint import pprint

client = MongoClient('127.0.0.1', 27017)

db = client['vacancies2806']

# hhru = db.hhru

# count = 0
# for doc in hhru.find({}):
#     pprint(doc)
#     count += 1

# hhru.delete_many({})

sjru = db.sjru

count = 0
for doc in sjru.find({}):
    pprint(doc)
    count += 1

# sjru.delete_many({})

print(count)
