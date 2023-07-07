# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from itemloaders.processors import MapCompose, TakeFirst, Compose


def srt_strip(value):
    return value.replace('\n', '').strip()


def clean_price(value):
    new_value = value.replace(' ', '')
    try:
        new_value = int(new_value)
    except:
        pass
    return new_value


def get_photos_list(photos_list):
    photos_to_download = []
    for photo in photos_list:
        if photo.startswith("/upload"):
            photo = 'https://www.castorama.ru' + photo
        photos_to_download.append(photo)
    return photos_to_download


def get_label_list(label_list):
    labels = []
    for label in label_list:
        labels.append(srt_strip(label))
    return labels


def get_value_list(value_list):
    values = []
    for value in value_list:
        values.append(srt_strip(value))
    return values


class CastoramaItem(scrapy.Item):
    # define the fields for your item here like:
    name = scrapy.Field(output_processor=TakeFirst(), input_processor=MapCompose(srt_strip))
    link = scrapy.Field(output_processor=TakeFirst())
    price = scrapy.Field(output_processor=TakeFirst(), input_processor=MapCompose(clean_price))
    photos = scrapy.Field(input_processor=Compose(get_photos_list))
    char_label = scrapy.Field(input_processor=Compose(get_label_list))
    char_value = scrapy.Field(input_processor=Compose(get_value_list))
    char_full = scrapy.Field()

