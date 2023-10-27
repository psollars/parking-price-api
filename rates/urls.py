from django.urls import include, path
from rest_framework import routers
from rates.views import PriceView, RateViewSet

ROUTER = routers.DefaultRouter()

ROUTER.register(r"rates", RateViewSet, basename="rates")
# ROUTER.register(r"price", PriceView.as_view(), basename="price")

rates_url_patterns = [
    path("", include(ROUTER.urls)),
    path("price/", PriceView.as_view(), name="price"),
]
