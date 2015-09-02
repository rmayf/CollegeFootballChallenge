# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('stats', '0001_initial'),
        ('leaderboard', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Picks',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('score', models.IntegerField(default=0)),
                ('D', models.ForeignKey(related_name='d', to='stats.Team')),
                ('K', models.ForeignKey(related_name='k', to='stats.Team')),
                ('QB1', models.ForeignKey(related_name='qb2', to='stats.Player')),
                ('RB1', models.ForeignKey(related_name='rb1', to='stats.Player')),
                ('RB2', models.ForeignKey(related_name='rb2', to='stats.Player')),
                ('WR1', models.ForeignKey(related_name='wr1', to='stats.Player')),
                ('WR2', models.ForeignKey(related_name='wr2', to='stats.Player')),
                ('user', models.ForeignKey(to='leaderboard.User_')),
                ('week', models.ForeignKey(to='stats.Week')),
            ],
        ),
    ]
