from rest_framework import serializers
from findCommonTimeToMeetApp.models import UserTimingPreferences


class UserTimingPreferencesSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserTimingPreferences
        fields = "__all__"
