from django.urls import path, include

urlpatterns = [
    path('user/', include('api.v1.user.urls')),
    path('userTimingPreferences/',
         include('api.v1.userTimingPreferences.urls'))
]
