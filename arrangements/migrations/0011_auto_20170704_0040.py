# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-07-03 16:40
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('arrangements', '0010_auto_20170704_0039'),
    ]

    operations = [
        migrations.AlterField(
            model_name='activity',
            name='start_time',
            field=models.DateTimeField(),
        ),
    ]