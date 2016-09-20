# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import base.models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='AccountStatistic',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('global_rating', models.IntegerField()),
                ('avg_damage_assisted', models.FloatField()),
                ('avg_damage_assisted_radio', models.FloatField()),
                ('avg_damage_assisted_track', models.FloatField()),
                ('avg_damage_blocked', models.FloatField()),
                ('battle_avg_xp', models.IntegerField()),
                ('capture_points', models.IntegerField()),
                ('damage_dealt', models.IntegerField()),
                ('damage_received', models.IntegerField()),
                ('direct_hits_received', models.IntegerField()),
                ('dropped_capture_points', models.IntegerField()),
                ('explosion_hits', models.IntegerField()),
                ('explosion_hits_received', models.IntegerField()),
                ('frags', models.IntegerField()),
                ('hits', models.IntegerField()),
                ('hits_percents', models.FloatField()),
                ('max_damage', models.IntegerField()),
                ('max_damage_tank_id', models.IntegerField()),
                ('max_frags', models.IntegerField()),
                ('max_frags_tank_id', models.IntegerField()),
                ('max_xp', models.IntegerField()),
                ('max_xp_tank_id', models.IntegerField()),
                ('shots', models.IntegerField()),
                ('spotted', models.IntegerField()),
                ('survived_battles', models.IntegerField()),
                ('draws', models.IntegerField()),
                ('losses', models.IntegerField()),
                ('wins', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='WotAccount',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('account_id', models.IntegerField(unique=True, db_index=True)),
                ('nickname', models.CharField(unique=True, max_length=256, db_index=True)),
            ],
        ),
        migrations.AlterModelManagers(
            name='user',
            managers=[
                ('objects', base.models.UserManager()),
            ],
        ),
        migrations.AddField(
            model_name='accountstatistic',
            name='account',
            field=models.ForeignKey(related_name='statistics', to='base.WotAccount', to_field=b'account_id'),
        ),
    ]
