# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-06-30 08:51
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('arrangements', '0006_auto_20170630_1522'),
    ]

    operations = [
        migrations.AlterField(
            model_name='activity',
            name='type',
            field=models.CharField(max_length=10),
        ),
    ]