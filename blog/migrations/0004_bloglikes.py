# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0003_comment'),
    ]

    operations = [
        migrations.CreateModel(
            name='BlogLikes',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, primary_key=True, verbose_name='ID')),
                ('likes', models.IntegerField(default=0, verbose_name='Нравится')),
                ('dislikes', models.IntegerField(default=0, verbose_name='Не нравится')),
            ],
        ),
    ]
