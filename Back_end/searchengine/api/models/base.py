import calendar

from django.contrib.auth.models import User as djUser
from django.db import models
from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank
from django.utils import timezone

from api.models import active_search


class Province(models.Model):
    name = models.CharField(max_length=25)

    def __str__(self):
       return self.name

    @classmethod
    def get_all(cls):
        return cls.objects.all()


class City(models.Model):
    name = models.CharField(max_length=25)
    province = models.ForeignKey(Province, on_delete=models.CASCADE)
    deleted = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    @classmethod
    def get_cities(cls, id):
        return cls.objects.filter(province_id=id)


class Source(models.Model):
    name = models.CharField(max_length=32)
    logo = models.ImageField(upload_to='source_logo', null=True, blank=True)
    fa_name = models.CharField(max_length=64)

    def __str__(self):
        return self.name


class AdsBase(models.Model):
    token = models.CharField(primary_key=True, max_length=18)
    time = models.IntegerField()

    class Meta:
        managed = False
        abstract = True

    @classmethod
    def search(cls, **data):
        search = None
        time = None
        if data.get('time', False):
            time = data.pop('time')
            if time < calendar.timegm(timezone.now().timetuple()) - 2592000:
                time = None
        if data.get('search', False):
            search = data.pop('search')
        if time is not None:
            result = cls.objects.filter(
            time__gte=time,
                    **data
            ).order_by('-time')
        else:
            result = cls.objects.filter(
            time__gte=calendar.timegm((timezone.now() - timezone.timedelta(days=30)).timetuple()),
            **data
            ).order_by('-time')
        if search is not None:
            vector = SearchVector('title', weight='A') + SearchVector('description', weight='B')
            query = SearchQuery(search)
            result = result.annotate(
            rank=SearchRank(vector, query)
            ).order_by('-rank', '-time')
        return result


class DeviceType(models.Model):
    name = models.CharField(max_length=16, unique=True)

    def __str__(self):
        return self.name


class NotificationsToken(models.Model):
    user = models.ForeignKey(djUser, on_delete=models.CASCADE, related_name='notification_user')
    device = models.ForeignKey(DeviceType, on_delete=models.CASCADE, related_name='notification_device')
    token = models.CharField(max_length=4096)

    class Meta:
        unique_together = (
        'user',
        'device'
        )

    def __str__(self):
        return self.token


class Banner(models.Model):
    image = models.ImageField(upload_to='banners/')
    alt = models.CharField(max_length=1024, null=True, blank=True)


class Favourite(models.Model):
    user = models.ForeignKey(djUser, on_delete=models.CASCADE)
    type = models.CharField(max_length=20, choices=active_search.TYPES)
    time = models.DateTimeField(auto_now_add=True)
    token = models.CharField(max_length=20)

    class Meta:
        unique_together = [
        (
        'user',
        'type',
        'token',
        ),
        ]