from django.urls import path
from . import views

urlpatterns = [
    path('', views.UserAPI.as_view()),
    path('<str:pk>', views.UserReRetrieveUpdateDestroyAPI.as_view())
]
