# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-05-09 07:28
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0016_auto_20160508_1613'),
    ]

    operations = [
        migrations.AddField(
            model_name='tag',
            name='important',
            field=models.BooleanField(default=False),
        ),
    ]