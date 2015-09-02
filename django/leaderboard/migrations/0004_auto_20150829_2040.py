# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('leaderboard', '0003_auto_20150829_1938'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user_',
            name='user',
        ),
        migrations.AlterField(
            model_name='picks',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
        ),
        migrations.DeleteModel(
            name='User_',
        ),
    ]
