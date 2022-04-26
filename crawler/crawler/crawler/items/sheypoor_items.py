from sre_constants import SRE_FLAG_ASCII
from crawler.items.items import BaseItem, RecruitmentBaseItem
from crawler.utilities.uses import hash_token, get_time_stamp


class SheypoorBaseItem(BaseItem):

    def extract(self, data):
        self['url'] = f"https://www.sheypoor.com/{data.css('#item-details > p.description::attr(data-reveal-description)').extract_first()}"
        self['token'] = hash_token(data.css('#item-details > p.description::attr(data-reveal-description)').extract_first(), 2)
        self['source_id'] = 2
        self['time'] = get_time_stamp()
        try:
            self['title'] = data.css('#item-details > div > h1::text').extract_first().strip()
        except:
            pass
        self['province'] = data.css('#breadcrumbs > ul > li:nth-child(2) > a::text').extract_first().strip().replace(
            '‌', ' ')
        self['city'] = data.css('#breadcrumbs > ul > li:nth-child(3) > a::text').extract_first().strip().replace('‌',
                                                                                                                 ' ')
        self['neighbourhood'] = 'not_defined'
        self['description'] = ''.join([item for item in data.css('#item-details > p.description::text').extract()])
        self['thumbnail'] = data.css('div[class="swiper-slide swiper-zoom-container"] img::attr(src)').extract_first()
        try:
            self['price'] = data.css("#item-details > p.text-left > span.clearfix.pull-left.text-right"
                                     " > span > strong::text").extract_first().replace(',', '')
        except:
            pass


class RecruitmentItem(RecruitmentBaseItem, SheypoorBaseItem):
    def clean_category(self, data):
        self['category'] = data.css('#breadcrumbs > ul > li:nth-child(5) > a::text').extract_first()
    def extract(self, data):
        SheypoorBaseItem.extract(self, data)
        try:
            self['advertiser'] = data.css('#item-seller-details > div > h3 strong::text').extract_first()
        except:
            pass
        self['description'] = ''.join([item for item in data.css('#item-details > p.description::text').extract()])
        self.clean_category(data)
        for i in data.css('#item-details > table.key-val'):
            for j in i.css('table > tr'):
                tmp = j.css('th::text').extract_first()
                if tmp == 'میزان تحصیلات':
                    try:
                        self['education'] = j.css('td::text').extract_first().strip()
                    except:
                        self['education'] = None

                elif tmp == 'جنسیت':
                    try:
                        gender = j.css('td::text').extract_first().strip()
                        if gender == 'فرقی نمیکند':
                           self['gender'] = None
                        else:    
                           self['gender'] = j.css('td::text').extract_first().strip()
                    except:
                        self['gender'] = None
                
                elif tmp == 'بیمه':
                    self['insurnace'] = 'دارد'
                
                elif tmp == 'نوع قرارداد':
                    try:
                        self['cooperation'] = j.css('td::text').extract_first().strip()
                    except:
                        self['cooperation'] = None

                elif tmp == 'میزان حقوق':
                    try:
                        salary = j.css('td::text').extract_first().strip()
                        if salary == 'مطابق وزارت کار':
                            self['salary'] = 0
                        elif salary == '۱ تا ۲.۵ میلیون تومان':
                            self['salary'] = 2000000
                        elif salary == '۲.۵ تا ۳.۵ میلیون تومان':
                            self['salary'] = 3000000
                        elif salary == '۳.۵ تا ۵ میلیون تومان':
                            self['salary'] == 4000000
                        elif salary == '۵ تا ۸ میلیون تومان':
                            self['salary'] == 6500000
                        elif salary == '۸ میلیون تومان به بالا':
                            self['salary'] == 8500000
                        else:
                            self['salary'] == 0
                    
                    except:
                        self['salary'] == 0
                


