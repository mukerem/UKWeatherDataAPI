from django.urls import path
from rest_framework.routers import DefaultRouter

from weather import views

app_name = 'weather'

router = DefaultRouter()

urlpatterns = [
    path('', views.WeatherListAPIView.as_view(), name='weather-list'),
]

urlpatterns += router.urls
