from random import randint

from django.utils import timezone


def password_generator():
    return randint(100000, 999999)


def five_minute_later():
    return timezone.now() + timezone.timedelta(minutes=5)


def five_minute_ago():
    return timezone.now() - timezone.timedelta(minutes=5)
