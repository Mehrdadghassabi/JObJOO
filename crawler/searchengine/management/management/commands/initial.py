import traceback

from django.core.management import BaseCommand
from management import models
from api import models as api_models
from ad_registration import models as ad_registration_models

from .provice_data import PROVINCE_DATA
from .bot_data import HOME_CATEGORY


class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        try:
            cost = int(input("active search cost per day: "))
            ACTIVE_SEARCH_COST_SETTING, is_exist = models.Setting.objects.get_or_create(
                key='ACTIVE_SEARCH_COST',
                defaults={
                    'key': 'ACTIVE_SEARCH_COST',
                    'value': cost
                }
            )
            if is_exist:
                ACTIVE_SEARCH_COST_SETTING.value = cost
                ACTIVE_SEARCH_COST_SETTING.save()
            for pIndex, pValue in PROVINCE_DATA.items():
                obj, create = api_models.Province.objects.get_or_create(name=pIndex)
                for city in pValue:
                    api_models.City.objects.get_or_create(name=city, province=obj)
            for hcIndex, hcValue in HOME_CATEGORY.items():
                obj, create = ad_registration_models.HomeCategory.objects.get_or_create(name=hcIndex)
                for subcategory in hcValue:
                    ad_registration_models.HomeSubcategory.objects.get_or_create(name=subcategory, category=obj)
        except:
            traceback.print_exc()
