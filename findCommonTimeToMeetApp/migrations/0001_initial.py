# Generated by Django 3.2.6 on 2021-08-14 16:26

import django.contrib.auth.models
from django.db import migrations, models
import django.db.models.deletion
import findCommonTimeToMeetApp.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserTimingPreferences',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('day_start_time', models.TimeField()),
                ('day_end_time', models.TimeField()),
                ('time_zone', models.CharField(max_length=100, validators=[findCommonTimeToMeetApp.models.validate_timezone])),
            ],
        ),
        migrations.CreateModel(
            name='CustomUser',
            fields=[
                ('user_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='auth.user')),
                ('timing_preferences', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='findCommonTimeToMeetApp.usertimingpreferences')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            bases=('auth.user',),
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
    ]
