from rest_framework.generics import (CreateAPIView,
                                     RetrieveUpdateDestroyAPIView)
from rest_framework.permissions import AllowAny

from findCommonTimeToMeetApp.models import UserTimingPreferences
from . import serializer


class UserTimingPreferencesAPI(CreateAPIView):
    serializer_class = serializer.UserTimingPreferencesSerializer
    permission_classes = (AllowAny, )


class UserTimingPreferencesRetrieveUpdateDestroyAPI(
      RetrieveUpdateDestroyAPIView):
    serializer_class = serializer.UserTimingPreferencesSerializer

    def get_queryset(self):
        return UserTimingPreferences.objects.filter(id=self.kwargs.get('pk',
                                                                       None))
