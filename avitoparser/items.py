# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from itemloaders.processors import MapCompose, TakeFirst, Compose


def clean_price(value):
    new_value = value.replace(' ', '')
    try:
        new_value = int(new_value)
    except:
        pass
    return new_value


def get_photos_list(photos_list):
    photos_fin = []
    for photo in photos_list:
        if photo.startswith("https"):
            photos_fin.append(photo)
    return photos_fin


class AvitoparserItem(scrapy.Item):
    # define the fields for your item here like:
    name = scrapy.Field(output_processor=TakeFirst())
    link = scrapy.Field(output_processor=TakeFirst())
    description = scrapy.Field(output_processor=TakeFirst())
    price = scrapy.Field(output_processor=TakeFirst(), input_processor=MapCompose(clean_price))
    photos = scrapy.Field(input_processor=Compose(get_photos_list))
