# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Game',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date', models.DateTimeField()),
            ],
        ),
        migrations.CreateModel(
            name='Player',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100)),
                ('number', models.IntegerField(default=0)),
                ('position', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='PlayerStat',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('completions', models.IntegerField(default=0)),
                ('attempts', models.IntegerField(default=0)),
                ('passingYards', models.IntegerField(default=0)),
                ('passingTD', models.IntegerField(default=0)),
                ('thrownInterceptions', models.IntegerField(default=0)),
                ('TD', models.IntegerField(default=0)),
                ('carries', models.IntegerField(default=0)),
                ('yards', models.IntegerField(default=0)),
                ('kickoffTD', models.IntegerField(default=0)),
                ('puntTD', models.IntegerField(default=0)),
                ('interceptionsTD', models.IntegerField(default=0)),
                ('interceptions', models.IntegerField(default=0)),
                ('receptions', models.IntegerField(default=0)),
                ('player', models.ForeignKey(to='stats.Player')),
            ],
        ),
        migrations.CreateModel(
            name='Season',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
            ],
        ),
        migrations.CreateModel(
            name='Team',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100)),
                ('espnId', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='TeamStat',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('FG', models.IntegerField(default=0)),
                ('FGAttempts', models.IntegerField(default=0)),
                ('PAT', models.IntegerField(default=0)),
                ('PATAttempts', models.IntegerField(default=0)),
                ('pointsAllowed', models.IntegerField(default=0)),
                ('team', models.ForeignKey(to='stats.Team')),
            ],
        ),
        migrations.CreateModel(
            name='Week',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('index', models.IntegerField(default=0)),
                ('games', models.ForeignKey(to='stats.Game')),
            ],
        ),
        migrations.AddField(
            model_name='season',
            name='weeks',
            field=models.ForeignKey(to='stats.Week'),
        ),
        migrations.AddField(
            model_name='player',
            name='team',
            field=models.ForeignKey(to='stats.Team'),
        ),
        migrations.AddField(
            model_name='game',
            name='opponent',
            field=models.ForeignKey(related_name='opponent', to='stats.Team'),
        ),
        migrations.AddField(
            model_name='game',
            name='team',
            field=models.ForeignKey(related_name='team', to='stats.Team'),
        ),
    ]
