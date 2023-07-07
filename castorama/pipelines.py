# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

# useful for handling different item types with a single interface
from itemadapter import ItemAdapter

import scrapy
from scrapy.pipelines.images import ImagesPipeline
# import hashlib
# from scrapy.utils.python import to_bytes
# from castorama.runner import search


def full_char(char_label, char_value):
    result = {}
    for i in range(len(char_label)):
        result[char_label[i]] = char_value[i]
    return result


class CastoramaPipeline:
    def process_item(self, item, spider):
        item['char_full'] = full_char(item['char_label'], item['char_value'])
        print()
        return item


class CastoramaphotosPipeline(ImagesPipeline):
    def get_media_requests(self, item, info):
        for img in item['photos']:
            try:
                yield scrapy.Request(img)
            except Exception as e:
                print(e)

    def item_completed(self, results, item, info):
        if results:
            item['photos'] = [itm[1] for itm in results if itm[0]]
        return item

    # def file_path(self, request, response=None, info=None, *, item=None):
    #     image_guid = hashlib.sha1(to_bytes(request.url)).hexdigest()
    #     return f"{search}/{image_guid}.jpg"
