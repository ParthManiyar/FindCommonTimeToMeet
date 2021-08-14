from rest_framework.generics import (ListCreateAPIView,
                                     RetrieveUpdateDestroyAPIView)
from rest_framework.permissions import AllowAny

from findCommonTimeToMeetApp.models import CustomUser
from . import serializer


class UserAPI(ListCreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = serializer.UserSerializer
    permission_classes = (AllowAny, )


class UserRetrieveUpdateDestroyAPI(RetrieveUpdateDestroyAPIView):
    serializer_class = serializer.UserSerializer

    def get_queryset(self):
        return CustomUser.objects.filter(id=self.kwargs.get('pk', None))
