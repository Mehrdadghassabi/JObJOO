# -*- coding: utf-8 -*-
import scrapy
import datetime
import json

from crawler.items.sheypoor_items import RecruitmentItem
from scrapy import signals


class SheypoorSpider(scrapy.Spider):
    custom_settings = {
        'DOWNLOAD_DELAY': 5
    }

    name = 'sheypoor'
    allowed_domains = ['sheypoor.com']
    category = ''
    _pages = 10
    sheypoor_page = 1
    request_time = -1
    last_id = None
    first_id = "-1"
    item_count = 0
    start_time = str(int(round((datetime.datetime.utcnow() - datetime.datetime(1970,1,1,0,0,0)).total_seconds(), 4))) + '.0000'


    def __init__(self, category='none', **kwargs):
        self.cat = category
        self.category = 'recruitment'
        self.seed = round((datetime.datetime.utcnow() - datetime.datetime(1970,1,1,0,0,0)).total_seconds(), 4)
        super().__init__(**kwargs)

    def start_requests(self):
        yield scrapy.Request(url=self.get_url(), callback=self.parse, headers=self.headers)

    def parse(self, response, page=1):
        ads = response.css("article[class='serp-item list '] a::attr(href)")
        ads += response.css("article[class='serp-item list shop-item'] a::attr(href)")
        self.logger.info(f"length of data:{len(ads)//2} for page:{page} and time is:{self.request_time}")

        for ad in set(ads.extract()):
            if page > self._pages:
                return None
            yield scrapy.Request(url=ad, 
                                 callback=self.parse_ad)

        if page < self._pages:
            yield response.follow(url=self.get_url(), callback=self.parse, cb_kwargs={"page": page + 1},
                                  headers=self.headers)

    def parse_ad(self, response):
        if self.category == 'recruitment':
            item = RecruitmentItem()
            item.extract(response)
            return item

        # return None

    def get_url(self):
        request_time = self.get_request_time()
        category_id = {
            "home": "ایران/املاک",
            "car": "ایران/وسایل-نقلیه",
            "recruitment": "ایران/استخدام"
        }
        if self.sheypoor_page == 1:
            return f"https://www.sheypoor.com/{category_id.get(self.category,'-1-')}"
        else:
            return f"https://www.sheypoor.com/{category_id.get(self.category,'-1-')}?p={self.sheypoor_page}&f={request_time}"

    def get_request_time(self):
        if self.request_time == -1 or self.sheypoor_page >= 25:
            self.sheypoor_page = 0
            self.request_time = str(self.start_time)[:15]
        self.sheypoor_page += 1
        return self.request_time


    category_list = [
        "املاک",
        "وسایل نقلیه"
        "ورزش فرهنگ فراغت",
        "لوازم الکترونیکی",
        "استخدام",
        "صنعتی، اداری و تجاری",
        "خدمات و کسب و کار",
        "موبایل، تبلت و لوازم",
        "لوازم خانگی",
        "لوازم شخصی",
    ]

    headers = {
        'Api-Version': 'v5.3.0',
        'App-Version': '5.3.15',
        'User-Agent': 'Android/5.1.1 Sheypoor/5.3.15 VersionCode/5031500 Manufacturer/samsung Model/SM-N950N',
        'Phone-Base': 'true',
        'X-AGENT-TYPE': 'Android App',
        'X-BUILD-MODE': 'Release',
        'X-FLAVOR': 'bazaar',
        'Unique-Id': '49e2bb9c-a7c3-3086-a858-b1e38fbf1fc5'
    }