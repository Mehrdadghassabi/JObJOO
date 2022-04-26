# Generated by Django 2.2.4 on 2020-09-26 11:57

import django.core.validators
from django.db import migrations, models
import tinymce.models


class Migration(migrations.Migration):

    dependencies = [
        ('management', '0003_robots'),
    ]

    operations = [
        migrations.CreateModel(
            name='AboutUs',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=256)),
                ('content', tinymce.models.HTMLField()),
            ],
        ),
        migrations.CreateModel(
            name='ContactUs',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=256)),
                ('phone', models.CharField(max_length=11, validators=[django.core.validators.MinLengthValidator(11), django.core.validators.MaxLengthValidator(11), django.core.validators.RegexValidator('^09[0-9]{9}$')])),
                ('content', models.TextField(validators=[django.core.validators.MaxLengthValidator(10240)])),
            ],
        ),
        migrations.AlterField(
            model_name='staticurlsitemap',
            name='url',
            field=models.CharField(blank=True, max_length=1024),
        ),
    ]
