import calendar

from django.db import models
from django.db.models import Min, Max, Count
from django.utils import timezone

from .base import AdsBase


class RecruimentAds(AdsBase):
    title = models.CharField(max_length=256, null=True)
    source = models.ForeignKey('api.Source', on_delete=models.DO_NOTHING) # source site name
    url = models.CharField(max_length=2048, null=True)
    thumbnail = models.CharField(max_length=2048, null=True)
    city = models.CharField(max_length=64, null=True)
    province = models.CharField(max_length=64, null=True)
    neighbourhood = models.CharField(max_length=64, null=True)
    education=models.CharField(max_length=64, null=True)
    gender=models.CharField(max_length=15, null=True)
    cooperation=models.CharField(max_length=64, null=True)
    salary=models.BigIntegerField(null=True)
    insurnace=models.CharField(max_length=15, null=True)
    category = models.CharField(max_length=64, null=True)
    sub_category = models.CharField(max_length=64, null=True)
    experience=models.IntegerField(null=True)
    description = models.CharField(max_length=4096, null=True)

    class Meta:
        managed = True
        db_table = 'recruiment'

    def __str__(self):
        return self.title

    def get_source(self):
        return self.source.name

    @classmethod
    def get_ranges(cls):
        recruiment=cls.objects.filter(
            time__gte=int(timezone.now().timestamp()) - 2592000
        ).aggregate(
            min_salary=Min('salary'),
            max_salary=Max('salary'),   
            min_experience=Min('experience'),
            max_experience=Max('experience'),
        )

        categories = cls.objects.filter(
                time__gte=int(timezone.now().timestamp()) - 2592000
                ).filter(category__isnull=False).distinct('category').values('category')

        education = cls.objects.filter(
                    time__gte=int(timezone.now().timestamp()) - 2592000
                ).filter(education__isnull=False).distinct('education').values('education')
        
        cooperation = cls.objects.filter(
                    time__gte=int(timezone.now().timestamp()) - 2592000
                ).filter(cooperation__isnull=False).distinct('cooperation').values('cooperation')

        gender = cls.objects.filter(
                    time__gte=int(timezone.now().timestamp()) - 2592000
                ).filter(gender__isnull=False).distinct('gender').values('gender')

        insurnace = cls.objects.filter(
                    time__gte=int(timezone.now().timestamp()) - 2592000
                ).filter(insurnace__isnull=False).distinct('insurnace').values('insurnace')
        
        return {
            'name': 'استخدام',
            'min_salary': recruiment['min_salary'],
            'max_salary': recruiment['max_salary'],
            'min_experience': recruiment['min_experience'],
            'max_experience': recruiment['max_experience'],
            'categories': [i['category'] for i in categories],
            'education' : [i['education'] for i in education],
            'cooperation' : [i['cooperation'] for i in cooperation],
            'gender' : [i['gender'] for i in gender],
            'insurnace' : [i['insurnace'] for i in insurnace]
        }
        
    @classmethod
    def get_by_id(cls, id):
        try:
            obj = cls.objects.get(token=id)
            return obj
        except cls.DoesNotExist:
            return None

    def similar(self):
        query = {
        'time__gte': calendar.timegm((timezone.now() - timezone.timedelta(days=15)).timetuple()),
        'province': self.province,
        'city': self.city,
        'category': self.category,
        'sub_category': self.sub_category,
        }

        if self.salary is not None and self.salary != 0:
            if self.salary <= 2000000:
                min = self.salary - 1000000
                max = self.salary + 1000000
            elif self.salary <= 5000000:
                min = self.salary - 2500000
                max = self.salary + 2500000
            else:
                min = self.salary - 5000000
                max = self.salary + 5000000

            query['salary__gte'] = min
            query['salary__lte'] = max
        
        if self.experience is not None and self.experience != 0:
            query['experience__gte'] = self.experience - 1
            query['experience__lte'] = self.experience + 10

        return RecruimentAds.objects.exclude(token=self.token).filter(
            **query
        ).order_by('-time')[:12]



