from django.urls import path
from . import views

urlpatterns = [
    path('', views.UserAPI.as_view()),
    path('<int:pk>', views.UserRetrieveUpdateDestroyAPI.as_view())
]
