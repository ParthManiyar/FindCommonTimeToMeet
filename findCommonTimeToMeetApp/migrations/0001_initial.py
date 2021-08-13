# Generated by Django 3.2.6 on 2021-08-13 16:14

from django.db import migrations, models
import django.db.models.deletion
import findCommonTimeToMeetApp.models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='UserTimingPreferences',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('day_start_time', models.DateTimeField()),
                ('day_end_time', models.DateTimeField()),
                ('time_zone', models.CharField(max_length=100, validators=[findCommonTimeToMeetApp.models.validate_timezone])),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('username', models.CharField(max_length=50, unique=True)),
                ('first_name', models.CharField(max_length=50)),
                ('last_name', models.CharField(max_length=50)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('password', models.CharField(max_length=128, null=True, verbose_name='password')),
                ('timingPreferences', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='findCommonTimeToMeetApp.usertimingpreferences')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
