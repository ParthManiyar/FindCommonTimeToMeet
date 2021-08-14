from django.db import models
from django.core.exceptions import ValidationError
import pytz
from django.contrib.auth.models import User


def validate_timezone(value):
    if value in pytz.all_timezones:
        return value
    else:
        raise ValidationError("This field accepts only valid time zone")


class UserTimingPreferences(models.Model):
    day_start_time = models.TimeField()
    day_end_time = models.TimeField()
    time_zone = models.CharField(max_length=100,
                                 validators=[validate_timezone])


class CustomUser(User):
    timing_preferences = models.ForeignKey(UserTimingPreferences,
                                           on_delete=models.CASCADE,
                                           null=False)
