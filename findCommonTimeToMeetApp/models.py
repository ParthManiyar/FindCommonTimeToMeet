from django.db import models
import uuid
from django.core.exceptions import ValidationError
import pytz


def validate_timezone(value):
    if pytz.all_timezones in value:
        return value
    else:
        raise ValidationError("This field accepts only valid time zone")


class TimestampModel(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class UserTimingPreferences(models.Model):
    id = models.UUIDField(primary_key=True,
                          default=uuid.uuid4,
                          editable=False)
    day_start_time = models.DateTimeField()
    day_end_time = models.DateTimeField()
    time_zone = models.CharField(max_length=100,
                                 validators=[validate_timezone])


class User(TimestampModel):
    id = models.UUIDField(primary_key=True,
                          default=uuid.uuid4,
                          editable=False)
    username = models.CharField(max_length=50, unique=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(max_length=254, unique=True)
    password = models.CharField('password', max_length=128, null=False)
    timingPreferences = models.ForeignKey(UserTimingPreferences,
                                          on_delete=models.CASCADE,
                                          null=False)

    def __str__(self):
        return self.username
