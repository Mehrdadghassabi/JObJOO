import os
from celery import Celery, platforms

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'searchengine.settings')

app = Celery('searchengine')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

platforms.C_FORCE_ROOT = True