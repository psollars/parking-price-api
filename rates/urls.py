from django.urls import include, path
from rest_framework import routers
from rates.views import RateViewSet

ROUTER = routers.DefaultRouter()

ROUTER.register("rates", RateViewSet, basename="rates")

rates_url_patterns = [path("", include(ROUTER.urls))]
