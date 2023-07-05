import requests
from lxml import html
from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError
from pprint import pprint


client = MongoClient('127.0.0.1', 27017)
db = client['users0507']
news = db.news

header = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 '
                  'Safari/537.36'
}

response = requests.get('https://lenta.ru/', headers=header)

dom = html.fromstring(response.text)

items = dom.xpath("//div[@class='topnews__column']/child::*")
for item in items:
    doc = {}
    name = item.xpath(".//h3[contains(@class, 'title')]/text()")
    date = item.xpath(".//div[contains(@class, 'info')]//text()")
    link = item.xpath(".//@href")
    if link[0].startswith('/news'):
        link[0] = 'https://lenta.ru' + link[0]

    doc['site'] = 'lenta.ru'
    doc['name'] = name[0]
    doc['date'] = date[0]
    doc['_id'] = link[0]

    try:
        news.insert_one(doc)
    except DuplicateKeyError:
        print(f"Дублирование {doc['_id']}")

for doc in news.find({}):
    pprint(doc)
