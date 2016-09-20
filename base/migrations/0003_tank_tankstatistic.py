# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import base.mixins


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0002_auto_20151118_1014'),
    ]

    operations = [
        migrations.CreateModel(
            name='Tank',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('tank_id', models.IntegerField(unique=True)),
                ('avg_draws', models.FloatField(default=0.0)),
                ('avg_losses', models.FloatField(default=0.0)),
                ('avg_wins', models.FloatField(default=0.0)),
                ('avg_frags', models.FloatField(default=0.0)),
                ('avg_survived_battles', models.FloatField(default=0.0)),
                ('probability_of_survival', models.FloatField(default=0.0)),
                ('probability_of_losses', models.FloatField(default=0.0)),
                ('probability_of_wins', models.FloatField(default=0.0)),
                ('probability_of_draws', models.FloatField(default=0.0)),
                ('accounts', models.ManyToManyField(related_name='tanks', to='base.WotAccount')),
            ],
        ),
        migrations.CreateModel(
            name='TankStatistic',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('mark_of_mastery', models.IntegerField()),
                ('max_frags', models.IntegerField()),
                ('max_xp', models.IntegerField()),
                ('avg_damage_blocked', models.FloatField()),
                ('battle_avg_xp', models.FloatField()),
                ('battles', models.FloatField()),
                ('capture_points', models.IntegerField()),
                ('damage_dealt', models.IntegerField()),
                ('damage_received', models.IntegerField()),
                ('draws', models.IntegerField()),
                ('losses', models.IntegerField()),
                ('wins', models.IntegerField()),
                ('frags', models.IntegerField()),
                ('survived_battles', models.IntegerField()),
                ('account', models.ForeignKey(to='base.WotAccount', to_field=b'account_id')),
                ('tank', models.ForeignKey(to='base.Tank', to_field=b'tank_id')),
            ],
            bases=(base.mixins.FieldsMixin, models.Model),
        ),
    ]
