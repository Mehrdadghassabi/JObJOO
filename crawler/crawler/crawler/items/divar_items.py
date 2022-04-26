from crawler.items.items import BaseItem, RecruitmentBaseItem
from crawler.utilities.Normalize import remove_extra_character_and_normalize
from crawler.utilities.Normalize import convert_alphabetic_number_to_integer, clean_number
from crawler.utilities.uses import hash_token, get_time_stamp, extract_model_brand
from unidecode import unidecode

class DivarBaseItem(BaseItem):
    def extract(self, dict_data):
        self['time'] = get_time_stamp()
        self['title'] = dict_data['data']['share']['title']
        self['description'] = dict_data['widgets']['description']
        self['token'] = hash_token(dict_data['token'], 1)
        self['source_id'] = 1
        self['url'] = dict_data['data']['url']
        image_list = dict_data['widgets']['web_images']
        self['thumbnail'] = (image_list[0][0]['src'].replace(
            'webp', 'jpg')) if len(image_list) > 0 else 'not_defined'
        self['latitude'] = float(
            dict_data['widgets']['location'].get('latitude', -1))
        self['longitude'] = float(
            dict_data['widgets']['location'].get('longitude', -1))
        self['neighbourhood'] = dict_data['widgets']['header']['place']


class RecruitmentItem(RecruitmentBaseItem, DivarBaseItem):

    def fetch_data(self, i):
        if 'نوع همکاری' in i['title']:
            self['cooperation'] = i['value']
        elif 'دستمزد' in i['title']:
            if 'از' in i['value'] and 'تا' in i['value']:
                tmp = unidecode(i['value']
                                        ).replace('z', ''
                                        ).replace('twmn', ''
                                        ).replace(',', ''
                                        ).strip(
                                        ).split('t')
                
                self['salary'] = (int(tmp[0].strip()) + int(tmp[1].strip())) // 2
            
            elif 'حداقل' in i['value']:
                self['salary'] = int(unidecode(i['value']
                                                    ).replace('Hdql', ''
                                                    ).replace('twmn', ''
                                                    ).replace(',', ''
                                                    ).replace(' ', ''
                                                    ).strip())

            elif 'حداکثر' in i['value']:
                self['salary'] = int(
                                     unidecode(i['value']
                                     ).replace('Hdkhthr', ''
                                     ).replace('twmn', ''
                                     ).replace(',', ''
                                     ).replace(' ', ''
                                     ).strip())
            elif 'تومان' in i['value']:
                self['salary'] = int(
                                     unidecode(i['value']
                                     ).replace('twmn', ''
                                     ).replace(',', ''
                                     ).replace(' ', ''
                                     ).strip())
        elif 'بیمه' in i['title']:
            self['insurnace'] = i['value']

        elif 'نیاز به سابقه' in i['title']:
            if 'از' in i['value'] and 'تا' in i['value']:
                tmp = unidecode(i['value']
                                        ).replace('z', ''
                                        ).replace('sl', ''
                                        ).replace(',', ''
                                        ).strip(
                                        ).split('t')
                self['experience'] = (int(tmp[0].strip()) + int(tmp[1].strip())) // 2
            elif 'حداقل' in i['value']:
                self['experience'] = int(
                                        unidecode(i['value']
                                        ).replace('Hdql', ''
                                        ).replace('sl', ''
                                        ).replace(' ', ''))
            elif 'حداکثر' in i['value']:
                self['experience'] = int(
                                     unidecode(i['value']
                                     ).replace('Hdkhthr', ''
                                     ).replace('sl', ''
                                     ).replace(',', ''
                                     ).replace(' ', ''
                                     ).strip())
            elif 'کم‌تر' in i['value']:
                self['experience'] = int(
                                     unidecode(i['value']
                                     ).replace('khmtr', ''
                                     ).replace('sl', ''
                                     ).replace('z', ''
                                     ).replace(',', ''
                                     ).replace(' ', ''
                                     ).strip())
            elif 'بیش از' in i['value']:
                self['experience'] = int(
                                     unidecode(i['value']
                                     ).replace('bysh', ''
                                     ).replace('sl', ''
                                     ).replace('z', ''
                                     ).replace(',', ''
                                     ).replace(' ', ''
                                     ).strip())                       
            elif 'سال' in i['value']:
                self['experience'] = int(
                                     unidecode(i['value']
                                     ).replace('sl', ''
                                     ).replace(',', ''
                                     ).replace(' ', ''
                                     ).strip())

    def extract(self, dict_data):
        DivarBaseItem.extract(self, dict_data)
        list_data = dict_data['widgets']['list_data']
        for i in list_data:
            if 'items' in i:
                for item in i['items']:
                    self.fetch_data(item)
            else:
                self.fetch_data(i)

