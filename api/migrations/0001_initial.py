# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-08-25 00:51
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Machine',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('accountId', models.IntegerField(help_text='The users lobby account ID, e.g. 521734.')),
                ('cpuName', models.CharField(help_text='CPU Family, e.g. "Intel i7-7700K CPU @ 4.20GHz".', max_length=128)),
                ('osFamily', models.CharField(help_text='The installed OS family, e.g. "Linux", "Mac OS", "Windows".', max_length=32)),
            ],
        ),
    ]
