from django.contrib.postgres.fields import JSONField
from django.contrib.auth.models import User as djUser
from django.db import models
from django.utils import timezone

from searchengine import settings

DATABASE = getattr(settings, 'DATABASES')['default']['ENGINE']

RECRUIMENT='recruiment'
TYPES = (
 (RECRUIMENT, 'recruiment'),
)


class ActiveSearchBase(models.Model):
    user = models.ForeignKey(djUser, on_delete=models.CASCADE,
    related_name="%(app_label)s_%(class)s_related",
    related_query_name="%(app_label)s_%(class)ss")
    name = models.CharField(max_length=128)
    filter = JSONField()
    raw_filter = JSONField()
    type = models.CharField(max_length=32, choices=TYPES)
    create_time = models.DateTimeField(auto_now_add=True)
    expire_time = models.DateTimeField()
    last_checked = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True

    def __str__(self):
        return self.user.username


class ActiveSearch(ActiveSearchBase):
    def is_active(self):
        return self.expire_time >= timezone.now()

    @classmethod
    def get_user_expired_searches(cls, user):
        return cls.objects.filter(user=user, expire_time__lte=timezone.now())

    @classmethod
    def get_user_searches(cls, user):
        return cls.objects.filter(user=user, expire_time__gt=timezone.now())

    @classmethod
    def is_owner(cls, user, pk):
        try:
            return cls.objects.get(user=user, id=pk)
        except cls.DoesNotExist:
            return False


class ActiveSearchHistory(ActiveSearchBase):
    @classmethod
    def get_user_searches(cls, user):
        return cls.objects.filter(user=user)