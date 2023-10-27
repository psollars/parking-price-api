from rest_framework import viewsets
from rates.models import Rate
from rates.serializers import RateSerializer


class RateViewSet(viewsets.ModelViewSet):
    queryset = Rate.objects.all()
    serializer_class = RateSerializer
