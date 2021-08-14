from django.urls import path
from . import views

urlpatterns = [
    path('', views.FindCommonTimeToMeetAPIView.as_view()),
]
