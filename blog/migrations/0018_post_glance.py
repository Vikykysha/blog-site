# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-05-10 16:31
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0017_tag_important'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='glance',
            field=models.BigIntegerField(blank=True, default=0),
        ),
    ]
