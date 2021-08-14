from django.urls import path
from . import views

urlpatterns = [
    path('', views.UserTimingPreferencesAPI.as_view()),
    path('<int:pk>',
         views.UserTimingPreferencesRetrieveUpdateDestroyAPI.as_view())
]
