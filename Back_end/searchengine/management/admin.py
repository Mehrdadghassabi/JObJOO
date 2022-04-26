from django.contrib import admin

from django.apps import apps

admin.site.index_template = 'memcache_status/admin_index.html'

for model in apps.get_app_config('management').get_models():
    admin.site.register(model)
