from django.contrib.sites.models import Site
from django.core.validators import (
    MinLengthValidator,
    MaxLengthValidator,
    RegexValidator
)
from django.db import models
from tinymce.models import HTMLField

from searchengine import settings

SITE_ID = getattr(settings, 'SITE_ID')


class Setting(models.Model):
    key = models.CharField(max_length=256)
    value = models.CharField(max_length=256)

    def __str__(self):
        return '{}: {}'.format(self.key, self.value)


class StaticUrlSitemap(models.Model):
    url = models.CharField(max_length=1024, blank=True)

    def __str__(self):
        return Site.objects.get(id=SITE_ID).domain + '/' + self.url


class Robots(models.Model):
    text = models.TextField()

    def __str__(self):
        return self.text


class AboutUs(models.Model):
    title = models.CharField(max_length=256)
    content = HTMLField()

    def __str__(self):
        return self.title


class ContactUs(models.Model):
    name = models.CharField(max_length=256)
    phone = models.CharField(
        max_length=11,
        validators=[
            MinLengthValidator(11),
            MaxLengthValidator(11),
            RegexValidator(
                r'^09[0-9]{9}$'
            )
        ]
    )
    content = models.TextField(
        validators=[
            MaxLengthValidator(10240)
        ]
    )
