# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('stats', '0001_initial'),
        ('leaderboard', '0002_picks'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='picks',
            options={'verbose_name_plural': 'picks'},
        ),
        migrations.AddField(
            model_name='picks',
            name='QB2',
            field=models.ForeignKey(related_name='qb2', default='1', to='stats.Player'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='picks',
            name='QB1',
            field=models.ForeignKey(related_name='qb1', to='stats.Player'),
        ),
    ]
