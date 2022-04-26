import scrapy

from cansoCrawler.items.items import BaseItem
from cansoCrawler.utilities.uses import get_time_stamp, hash_token


class Item(BaseItem):
    code = scrapy.Field()

    def extract(self, dict_data):
        self['time'] = get_time_stamp()
        self['code'] = dict_data['id']
        self['token'] = hash_token(dict_data['id'], 9)
        self['title'] = dict_data['title']
        self['description'] = dict_data['content']
        self['tell'] = dict_data['phone']
        self['url'] = dict_data['link']
