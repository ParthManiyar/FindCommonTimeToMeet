from rest_framework import serializers
from findCommonTimeToMeetApp.models import UserTimingPreferences


class UserTimingPreferencesSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserTimingPreferences
        fields = "__all__"

    def validate(self, data):
        if data['day_start_time'] >= data['day_end_time']:
            raise serializers.ValidationError("day_start_time should "
                                              "be less than day_end_time")
        return data
