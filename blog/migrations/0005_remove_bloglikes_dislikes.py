# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0004_bloglikes'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='bloglikes',
            name='dislikes',
        ),
    ]
