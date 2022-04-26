import datetime
from persiantools.jdatetime import JalaliDate


def hash_token(token, source_id):
    import hashlib
    token = f"{token}{source_id}"
    return int(str(int(hashlib.sha1(str(token).encode()).hexdigest(), 16))[:18])


def get_time_stamp():
    return int(datetime.datetime.now().timestamp())


def get_persian_year():
    return int(JalaliDate.today().year)


def get_production(age):
    if age is None or age == -1 or age == '-1':
        return -1
    else:
        return get_persian_year() - int(age)


def extract_model_brand(self, brand_model):
    i = dict()
    i['value'] = brand_model
    if 'پراید' in i['value'] and '111' in i['value']:
        self['brand'] = 'پراید'
        self['model'] = '111'
    elif 'پراید' in i['value'] and '131' in i['value']:
        self['brand'] = 'پراید'
        self['model'] = '131'
    elif 'پراید' in i['value'] and '132' in i['value']:
        self['brand'] = 'پراید'
        self['model'] = '132'
    elif 'پراید' in i['value'] and '141' in i['value']:
        self['brand'] = 'پراید'
        self['model'] = '141'
    elif 'پراید' in i['value'] and 'اتوماتیک' in i['value']:
        self['brand'] = 'پراید'
        self['model'] = 'سایر مدل‌ها'
    elif 'پراید' in i['value'] and 'سفری' in i['value']:
        self['brand'] = 'پراید'
        self['model'] = 'سایر مدل‌ها'
    elif 'پراید' in i['value'] and 'صندوق‌دار' in i['value']:
        self['brand'] = 'پراید'
        self['model'] = 'صندوق‌دار'
    elif 'پراید' in i['value'] and 'هاچبک' in i['value']:
        self['brand'] = 'پراید'
        self['model'] = 'هاچبک'
    elif ('وانت' in i['value'] or '151' in i['value']) and 'پراید' in i['value']:
        self['brand'] = 'پراید'
        self['model'] = 'وانت'
    elif 'پراید' in i['value']:
        self['brand'] = 'پراید'
        self['model'] = 'سایر مدل‌ها'

    elif 'تیبا' in i['value'] and 'صندوق‌دار' in i['value'] or 'تیبا' in i['value'] and '1' in i['value']:
        self['brand'] = 'تیبا'
        self['model'] = 'صندوق دار'
    elif 'تیبا' in i['value'] and 'هاچبک' in i['value'] or 'تیبا' in i['value'] and '2' in i['value']:
        self['brand'] = 'تیبا'
        self['model'] = 'هاچ بک'
    elif 'تیبا' in i['value']:
        self['brand'] = 'تیبا'
        self['model'] = '‌سایر مدل‌ها'

    elif 'آریو' in i['value'] and 'اتوماتیک' in i['value'] and '1600cc' in i['value']:
        self['brand'] = 'آریو'
        self['model'] = 'آریو'
    elif 'دنده‌ای' in i['value'] and '1500cc' in i['value']:
        self['brand'] = 'آریو'
        self['model'] = 'آریو'
    elif 'دنده‌ای' in i['value'] and '1600cc' in i['value']:
        self['brand'] = 'آریو'
        self['model'] = 'آریو'
    elif 'آریو' in i['value']:
        self['brand'] = 'آریو'
        self['model'] = 'آریو'

    elif 'ساینا' in i['value'] and 'اتوماتیک' in i['value']:
        self['brand'] = 'ساینا'
        self['model'] = 'اتوماتیک'
    elif 'ساینا' in i['value'] and 'دنده‌ای' in i['value']:
        self['brand'] = 'ساینا'
        self['model'] = 'دنده ای'
    elif 'ساینا' in i['value']:
        self['brand'] = 'ساینا'
        self['model'] = 'سایر مدل‌ها'

    elif 'ام وی ام' in i['value'] and '110' in i['value']:
        self['brand'] = 'ام وی ام'
        self['model'] = '110'
    elif 'ام وی ام' in i['value'] and '110S' in i['value']:
        self['brand'] = 'ام وی ام'
        self['model'] = '110S'
    elif 'ام وی ام' in i['value'] and '315' in i['value'] and 'صندوق‌دار' in i['value']:
        self['brand'] = 'ام وی ام'
        self['model'] = '315 صندوق‌دار'
    elif 'ام وی ام' in i['value'] and '315' in i['value'] and 'هاچبک' in i['value']:
        self['brand'] = 'ام وی ام'
        self['model'] = '315 هاچبک'
    elif 'ام وی ام' in i['value'] and '530' in i['value']:
        self['brand'] = 'ام وی ام'
        self['model'] = '530'
    elif 'ام وی ام' in i['value'] and '550' in i['value']:
        self['brand'] = 'ام وی ام'
        self['model'] = '550'
    elif 'ام وی ام' in i['value'] and 'X33' in i['value']:
        self['brand'] = 'ام وی ام'
        self['model'] = 'X33'
    elif 'ام وی ام' in i['value'] and 'X22' in i['value']:
        self['brand'] = 'ام وی ام'
        self['model'] = 'X22'
    elif 'ام وی ام' in i['value'] and 'X33' in i['value'] and 'S' in i['value']:
        self['brand'] = 'ام وی ام'
        self['model'] = 'X33 S'
    elif 'ام وی ام' in i['value']:
        self['brand'] = 'ام وی ام'
        self['model'] = '‌سایر مدل‌ها'

    elif 'پژو' in i['value'] and '2008' in i['value']:
        self['brand'] = 'پژو'
        self['model'] = '2008'
    elif 'پژو' in i['value'] and '205' in i['value']:
        self['brand'] = 'پژو'
        self['model'] = '205'
    elif 'پژو' in i['value'] and '206' in i['value']:
        self['brand'] = 'پژو'
        self['model'] = '206'
    elif 'پژو' in i['value'] and '206' in i['value'] and 'SD' in i['value']:
        self['brand'] = 'پژو'
        self['model'] = '206 SD'
    elif 'پژو' in i['value'] and '207' in i['value']:
        self['brand'] = 'پژو'
        self['model'] = '207'
    elif 'پژو' in i['value'] and '301' in i['value']:
        self['brand'] = 'پژو'
        self['model'] = '301'
    elif 'پژو' in i['value'] and '404' in i['value']:
        self['brand'] = 'پژو'
        self['model'] = '404'
    elif 'پژو' in i['value'] and '405' in i['value']:
        self['brand'] = 'پژو'
        self['model'] = '405'
    elif 'پژو' in i['value'] and '406' in i['value']:
        self['brand'] = 'پژو'
        self['model'] = '406'
    elif 'پژو' in i['value'] and '407' in i['value']:
        self['brand'] = 'پژو'
        self['model'] = '407'
    elif 'پژو' in i['value'] and '504' in i['value']:
        self['brand'] = 'پژو'
        self['model'] = '504'
    elif 'پژو' in i['value'] and '508' in i['value']:
        self['brand'] = 'پژو'
        self['model'] = '508'
    elif 'پژو' in i['value'] and 'پارس' in i['value']:
        self['brand'] = 'پژو'
        self['model'] = 'پارس'
    elif 'پژو' in i['value'] and 'پارس' in i['value'] and 'لیموزین' in i['value']:
        self['brand'] = 'پژو'
        self['model'] = 'پارس لیموزین'
    elif 'پژو' in i['value'] and 'روآ' in i['value']:
        self['brand'] = 'پژو'
        self['model'] = 'روآ'
    elif 'پژو' in i['value'] and 'روآ' in i['value'] and 'سال' in i['value']:
        self['brand'] = 'پژو'
        self['model'] = 'روآ'
    elif 'پژو' in i['value'] and 'RD' in i['value']:
        self['brand'] = 'پژو'
        self['model'] = 'RD'
    elif 'پژو' in i['value'] and 'RDI' in i['value']:
        self['brand'] = 'پژو'
        self['model'] = 'RDI'
    elif 'پژو' in i['value']:
        self['brand'] = 'پژو'
        self['model'] = '‌سایر مدل‌ها'

    elif 'پیکان' in i['value'] and 'وانت' in i['value']:
        self['brand'] = 'پیکان'
        self['model'] = 'وانت'
    elif 'پیکان' in i['value']:
        self['brand'] = 'پیکان'
        self['model'] = 'سواری'

    elif 'دنا' in i['value'] and 'پلاس' in i['value']:
        self['brand'] = 'دنا'
        self['model'] = 'پلاس'
    elif 'دنا' in i['value'] and 'معمولی' in i['value']:
        self['brand'] = 'دنا'
        self['model'] = 'معمولی'
    elif 'دنا' in i['value']:
        self['brand'] = 'دنا'
        self['model'] = '‌سایر مدل‌ها'

    elif 'رانا' in i['value'] and 'EL' in i['value']:
        self['brand'] = 'رانا'
        self['model'] = 'رانا EL'
    elif 'رانا' in i['value'] and 'LX' in i['value']:
        self['brand'] = 'رانا'
        self['model'] = 'رانا LX'
    elif 'رانا' in i['value']:
        self['brand'] = 'رانا'
        self['model'] = 'سایر مدل ها'

    elif 'سمند' in i['value'] and 'سریر' in i['value']:
        self['brand'] = 'سمند'
        self['model'] = 'سریر'
    elif 'سمند' in i['value'] and 'سورن' in i['value']:
        self['brand'] = 'سمند'
        self['model'] = 'سورن'
    elif 'سمند' in i['value'] and 'EL' in i['value']:
        self['brand'] = 'سمند'
        self['model'] = 'EL'
    elif 'سمند' in i['value'] and 'LX' in i['value']:
        self['brand'] = 'سمند'
        self['model'] = 'LX'
    elif 'سمند' in i['value'] and 'SE' in i['value']:
        self['brand'] = 'سمند'
        self['model'] = 'SE'
    elif 'سمند' in i['value'] and 'X7' in i['value']:
        self['brand'] = 'سمند'
        self['model'] = 'X7'
    elif 'سمند' in i['value']:
        self['brand'] = 'سمند'
        self['model'] = '‌سایر مدل‌ها'

    elif 'وانت' in i['value'] and 'آریسان' in i['value'] and 'آریسان' in i['value']:
        self['brand'] = 'آریسان'
        self['model'] = 'وانت'
    elif 'وانت' in i['value'] and 'آریسان' in i['value']:
        self['brand'] = 'آریسان'
        self['model'] = 'وانت'

    elif 'هایما' in i['value'] and 'S5' in i['value']:
        self['brand'] = 'هایما'
        self['model'] = 'هایما S5'
    elif 'هایما' in i['value'] and 'S7' in i['value']:
        self['brand'] = 'هایما'
        self['model'] = 'هایما S7'
    elif 'هایما' in i['value']:
        self['brand'] = 'هایما'
        self['model'] = '‌سایر مدل‌ها'

    elif 'جک' in i['value'] and 'J3' in i['value'] and 'سدان' in i['value']:
        self['brand'] = 'جک'
        self['model'] = 'J3 سدان'
    elif 'جک' in i['value'] and 'J3' in i['value'] and 'هاچبک' in i['value']:
        self['brand'] = 'جک'
        self['model'] = 'J3 هاچبک'
    elif 'جک' in i['value'] and 'J4' in i['value']:
        self['brand'] = 'جک'
        self['model'] = 'J4'
    elif 'جک' in i['value'] and 'J5' in i['value']:
        self['brand'] = 'جک'
        self['model'] = 'J5'
    elif 'جک' in i['value'] and 'S3' in i['value']:
        self['brand'] = 'جک'
        self['model'] = 'S3'
    elif 'جک' in i['value'] and 'S5' in i['value']:
        self['brand'] = 'جک'
        self['model'] = 'S5'
    elif 'جک' in i['value']:
        self['brand'] = 'جک'
        self['model'] = '‌سایر مدل‌ها'

    elif 'جیلی' in i['value'] and 'Emgrand' in i['value'] and '7' in i['value']:
        self['brand'] = 'جیلی'
        self['model'] = 'امگرند 7'
    elif 'جیلی' in i['value'] and 'Emgrand' in i['value'] and '7_RV' in i['value']:
        self['brand'] = 'جیلی'
        self['model'] = 'امگرند آر وی 7'
    elif 'جیلی' in i['value'] and 'Emgrand' in i['value'] and 'X7' in i['value']:
        self['brand'] = 'جیلی'
        self['model'] = 'امگرند ایکس 7'
    elif 'جیلی' in i['value'] and 'GC6' in i['value']:
        self['brand'] = 'جیلی'
        self['model'] = 'GC6'
    elif 'جیلی' in i['value']:
        self['brand'] = 'جیلی'
        self['model'] = '‌سایر مدل‌ها'

    elif 'لیفان' in i['value'] and '520' in i['value']:
        self['brand'] = 'لیفان'
        self['model'] = 'لیفان 520'
    elif 'لیفان' in i['value'] and '520i' in i['value']:
        self['brand'] = 'لیفان'
        self['model'] = 'لیفان 520i'
    elif 'لیفان' in i['value'] and '620' in i['value']:
        self['brand'] = 'لیفان'
        self['model'] = 'لیفان 620'
    elif 'لیفان' in i['value'] and '820' in i['value']:
        self['brand'] = 'لیفان'
        self['model'] = 'لیفان 820'
    elif 'لیفان' in i['value'] and 'X50' in i['value']:
        self['brand'] = 'لیفان'
        self['model'] = 'لیفان X50'
    elif 'لیفان' in i['value'] and 'X60' in i['value']:
        self['brand'] = 'لیفان'
        self['model'] = 'لیفان X60'
    elif 'لیفان' in i['value']:
        self['brand'] = 'لیفان'
        self['model'] = 'سایر مدل‌ها'

    elif 'رنو' in i['value'] and '21' in i['value']:
        self['brand'] = 'رنو'
        self['model'] = '21'
    elif 'رنو' in i['value'] and '5' in i['value']:
        self['brand'] = 'رنو'
        self['model'] = '5'
    elif 'رنو' in i['value'] and '5' in i['value'] and 'مونتاژ' in i['value']:
        self['brand'] = 'رنو'
        self['model'] = '5 مونتاژ'
    elif 'رنو' in i['value'] and 'اسکالا' in i['value']:
        self['brand'] = 'رنو'
        self['model'] = 'اسکالا'
    elif 'رنو' in i['value'] and 'پارس' in i['value'] and 'تندر' in i['value']:
        self['brand'] = 'رنو'
        self['model'] = 'پارس تندر'
    elif 'رنو' in i['value'] and 'پی' in i['value'] and 'کی' in i['value']:
        self['brand'] = 'رنو'
        self['model'] = 'پی کی'
    elif 'رنو' in i['value'] and 'تلیسمان' in i['value']:
        self['brand'] = 'رنو'
        self['model'] = 'تلیسمان'
    elif 'رنو' in i['value'] and 'تندر' in i['value'] and '90' in i['value']:
        self['brand'] = 'رنو'
        self['model'] = 'تندر 90'
    elif 'رنو' in i['value'] and 'تندر' in i['value'] and '90' in i['value'] and 'پلاس' in i['value']:
        self['brand'] = 'رنو'
        self['model'] = '  تندر 90 پلاس'
    elif 'رنو' in i['value'] and 'داستر' in i['value']:
        self['brand'] = 'رنو'
        self['model'] = 'داستر'
    elif 'رنو' in i['value'] and 'ساندرو' in i['value']:
        self['brand'] = 'رنو'
        self['model'] = 'ساندرو'
    elif 'رنو' in i['value'] and 'ساندرو' in i['value'] and 'استپ‌وی' in i['value']:
        self['brand'] = 'رنو'
        self['model'] = 'ساندرو استپ وی'
    elif 'رنو' in i['value'] and 'سپند' in i['value']:
        self['brand'] = 'رنو'
        self['model'] = 'سپند'
    elif 'رنو' in i['value'] and 'سفران' in i['value']:
        self['brand'] = 'رنو'
        self['model'] = 'سفران'
    elif 'رنو' in i['value'] and 'سیمبل' in i['value']:
        self['brand'] = 'رنو'
        self['model'] = 'سیمبل'
    elif 'رنو' in i['value'] and 'فلوئنس' in i['value']:
        self['brand'] = 'رنو'
        self['model'] = 'فلوئنس'
    elif 'رنو' in i['value'] and 'کپچر' in i['value']:
        self['brand'] = 'رنو'
        self['model'] = 'کپچر'
    elif 'رنو' in i['value'] and 'کوليوس' in i['value']:
        self['brand'] = 'رنو'
        self['model'] = 'کوليوس'
    elif 'رنو' in i['value'] and 'لاگونا' in i['value']:
        self['brand'] = 'رنو'
        self['model'] = 'لاگونا'
    elif 'رنو' in i['value'] and 'لتیتود' in i['value']:
        self['brand'] = 'رنو'
        self['model'] = 'لتیتود'
    elif 'رنو' in i['value'] and 'مگان' in i['value']:
        self['brand'] = 'رنو'
        self['model'] = 'مگان'
    elif 'رنو' in i['value'] and 'مگان' in i['value'] and 'مونتاژ' in i['value']:
        self['brand'] = 'رنو'
        self['model'] = 'مگان مونتاژ'
    elif 'وانت' in i['value'] and 'رنو' in i['value'] and 'وانت' in i['value'] and 'تندر' in i['value'] and '91' in i[
        'value']:
        self['brand'] = 'رنو'
        self['model'] = 'وانت رنو وانت تندر 90'
    elif 'رنو' in i['value']:
        self['brand'] = 'رنو'
        self['model'] = '‌سایر مدل‌ها'

    elif 'برلیانس' in i['value'] and 'کراس' in i['value']:
        self['brand'] = 'برلیانس'
        self['model'] = 'کراس'
    elif 'برلیانس' in i['value'] and 'H220' in i['value']:
        self['brand'] = 'برلیانس'
        self['model'] = 'H220'
    elif 'برلیانس' in i['value'] and 'H230' in i['value']:
        self['brand'] = 'برلیانس'
        self['model'] = 'H230'
    elif 'برلیانس' in i['value'] and 'H320' in i['value']:
        self['brand'] = 'برلیانس'
        self['model'] = 'H320'
    elif 'برلیانس' in i['value'] and 'H330' in i['value']:
        self['brand'] = 'برلیانس'
        self['model'] = 'H330'
    elif 'برلیانس' in i['value'] and 'V5' in i['value']:
        self['brand'] = 'برلیانس'
        self['model'] = 'V5'
    elif 'برلیانس' in i['value']:
        self['brand'] = 'برلیانس'
        self['model'] = '‌سایر مدل‌ها'

    elif 'هیوندای' in i['value'] and 'آزرا' in i['value'] and 'گرنجور' in i['value']:
        self['brand'] = 'هیوندای'
        self['model'] = 'آزرا گرنجور'
    elif 'هیوندای' in i['value'] and 'آوانته' in i['value']:
        self['brand'] = 'هیوندای'
        self['model'] = 'آوانته'
    elif 'هیوندای' in i['value'] and 'اسکوپ' in i['value']:
        self['brand'] = 'هیوندای'
        self['model'] = 'اسکوپ'
    elif 'هیوندای' in i['value'] and 'اکسل' in i['value']:
        self['brand'] = 'هیوندای'
        self['model'] = 'اکسل'
    elif 'هیوندای' in i['value'] and 'اکسنت' in i['value']:
        self['brand'] = 'هیوندای'
        self['model'] = 'اکسنت'
    elif 'هیوندای' in i['value'] and 'اکسنت' in i['value'] and 'مونتاژ' in i['value']:
        self['brand'] = 'هیوندای'
        self['model'] = 'اکسنت مونتاژ'
    elif 'هیوندای' in i['value'] and 'النترا' in i['value']:
        self['brand'] = 'هیوندای'
        self['model'] = 'النترا'
    elif 'هیوندای' in i['value'] and 'النترا' in i['value'] and 'مونتاژ' in i['value']:
        self['brand'] = 'هیوندای'
        self['model'] = 'النترا مونتاژ'
    elif 'هیوندای' in i['value'] and 'تراجت' in i['value']:
        self['brand'] = 'هیوندای'
        self['model'] = 'تراجت'
    elif 'هیوندای' in i['value'] and 'توسان' in i['value'] and 'ix' in i['value'] and '35' in i['value']:
        self['brand'] = 'هیوندای'
        self['model'] = 'توسان ix 34'
    elif 'هیوندای' in i['value'] and 'جنسیس' in i['value'] and 'سدان' in i['value']:
        self['brand'] = 'هیوندای'
        self['model'] = 'جنسیس سدان'
    elif 'هیوندای' in i['value'] and 'جنسیس' in i['value'] and 'کوپه' in i['value']:
        self['brand'] = 'هیوندای'
        self['model'] = 'جنسیس کوپه'
    elif 'هیوندای' in i['value'] and 'سانتافه' in i['value']:
        self['brand'] = 'هیوندای'
        self['model'] = 'سانتافه'
    elif 'هیوندای' in i['value'] and 'سنتنیال' in i['value']:
        self['brand'] = 'هیوندای'
        self['model'] = 'سنتنیال'
    elif 'هیوندای' in i['value'] and 'سوناتا' in i['value'] and 'LF' in i['value']:
        self['brand'] = 'هیوندای'
        self['model'] = 'سوناتا LF'
    elif 'هیوندای' in i['value'] and 'سوناتا' in i['value'] and 'LF' in i['value'] and 'هیبرید' in i['value']:
        self['brand'] = 'هیوندای'
        self['model'] = 'سوناتا LF هیبرید'
    elif 'هیوندای' in i['value'] and 'سوناتا' in i['value'] and 'NF' in i['value']:
        self['brand'] = 'هیوندای'
        self['model'] = '‌سایر مدل‌ها'
    elif 'هیوندای' in i['value'] and 'سوناتا' in i['value'] and 'YF' in i['value']:
        self['brand'] = 'هیوندای'
        self['model'] = '‌سایر مدل‌ها'
    elif 'هیوندای' in i['value'] and 'سوناتا' in i['value'] and 'YF' in i['value']:
        self['brand'] = 'هیوندای'
        self['model'] = '‌سایر مدل‌ها'
    elif 'هیوندای' in i['value'] and 'وراکروز' in i['value'] and 'ix55' in i['value']:
        self['brand'] = 'هیوندای'
        self['model'] = 'وراکروز ix54‌'
    elif 'هیوندای' in i['value'] and 'ورنا' in i['value']:
        self['brand'] = 'هیوندای'
        self['model'] = 'ورنا'
    elif 'هیوندای' in i['value'] and 'ولستر' in i['value']:
        self['brand'] = 'هیوندای'
        self['model'] = 'ولستر'
    elif 'هیوندای' in i['value'] and 'FX' in i['value'] and 'کوپه' in i['value']:
        self['brand'] = 'هیوندای'
        self['model'] = 'FX کوپه'
    elif 'هیوندای' in i['value'] and 'i10' in i['value'] and 'مونتاژ' in i['value']:
        self['brand'] = 'هیوندای'
        self['model'] = 'i10 مونتاژ'
    elif 'هیوندای' in i['value'] and 'i20' in i['value']:
        self['brand'] = 'هیوندای'
        self['model'] = 'i20'
    elif 'هیوندای' in i['value'] and 'i30' in i['value']:
        self['brand'] = 'هیوندای'
        self['model'] = 'i30'
    elif 'هیوندای' in i['value'] and 'i40' in i['value']:
        self['brand'] = 'هیوندای'
        self['model'] = 'i40'
    elif 'هیوندای' in i['value'] and 'i40' in i['value'] and 'استیشن' in i['value']:
        self['brand'] = 'هیوندای'
        self['model'] = 'i40 استیشن'
    elif 'هیوندای' in i['value']:
        self['brand'] = 'هیوندای'
        self['model'] = '‌سایر مدل‌ها'

    elif 'کیا' in i['value'] and 'اپتیما' in i['value']:
        self['brand'] = 'کیا'
        self['model'] = 'اپتیما'
    elif 'کیا' in i['value'] and 'اپیروس' in i['value']:
        self['brand'] = 'کیا'
        self['model'] = 'اپیروس'
    elif 'کیا' in i['value'] and 'اسپورتیج' in i['value']:
        self['brand'] = 'کیا'
        self['model'] = 'اسپورتیج'
    elif 'کیا' in i['value'] and 'پیکانتو' in i['value']:
        self['brand'] = 'کیا'
        self['model'] = 'پیکانتو'
    elif 'کیا' in i['value'] and 'ریو' in i['value']:
        self['brand'] = 'کیا'
        self['model'] = 'ریو'
    elif 'کیا' in i['value'] and 'ریو' in i['value'] and 'مونتاژ' in i['value']:
        self['brand'] = 'کیا'
        self['model'] = 'ریو مونتاژ'
    elif 'کیا' in i['value'] and 'سراتو' in i['value']:
        self['brand'] = 'کیا'
        self['model'] = 'سراتو'
    elif 'کیا' in i['value'] and 'سراتو' in i['value'] and 'کوپه' in i['value']:
        self['brand'] = 'کیا'
        self['model'] = 'سراتو کوپه'
    elif 'کیا' in i['value'] and 'سراتو' in i['value'] and 'مونتاژ' in i['value']:
        self['brand'] = 'کیا'
        self['model'] = 'سراتو مونتاژ'
    elif 'کیا' in i['value'] and 'سورنتو' in i['value']:
        self['brand'] = 'کیا'
        self['model'] = 'سورنتو'
    elif 'کیا' in i['value'] and 'سول' in i['value']:
        self['brand'] = 'کیا'
        self['model'] = 'سول'
    elif 'کیا' in i['value'] and 'کادنزا' in i['value']:
        self['brand'] = 'کیا'
        self['model'] = 'کادنزا'
    elif 'کیا' in i['value'] and 'کارناوال' in i['value']:
        self['brand'] = 'کیا'
        self['model'] = 'کارناوال'
    elif 'کیا' in i['value'] and 'کارنز' in i['value']:
        self['brand'] = 'کیا'
        self['model'] = 'کارنز'
    elif 'کیا' in i['value'] and 'موهاوی' in i['value']:
        self['brand'] = 'کیا'
        self['model'] = 'موهاوی'
    elif 'کیا' in i['value']:
        self['brand'] = 'کیا'
        self['model'] = '‌سایر مدل‌ها'

    elif 'بسترن' in i['value'] and 'B30' in i['value']:
        self['brand'] = 'بسترن'
        self['model'] = 'B30'
    elif 'بسترن' in i['value'] and 'B50' in i['value']:
        self['brand'] = 'بسترن'
        self['model'] = 'B50'
    elif 'بسترن' in i['value'] and 'B50F' in i['value']:
        self['brand'] = 'بسترن'
        self['model'] = 'B50F'
    elif 'بسترن' in i['value']:
        self['brand'] = 'بسترن'
        self['model'] = '‌سایر مدل‌ها'

    else:
        self['brand'] = "not_defined"
        self['model'] = "not_defined"
