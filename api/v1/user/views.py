from rest_framework.generics import (ListCreateAPIView,
                                     RetrieveUpdateDestroyAPIView)
from rest_framework.permissions import AllowAny

from findCommonTimeToMeetApp.models import User
from . import serializer


class UserAPI(ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = serializer.UserSerializer
    permission_classes = (AllowAny, )


class UserReRetrieveUpdateDestroyAPI(RetrieveUpdateDestroyAPIView):
    serializer_class = serializer.UserSerializer

    def get_queryset(self):
        return User.objects.filter(id = self.kwargs.get('pk', None))
