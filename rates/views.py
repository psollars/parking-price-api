from datetime import datetime
from pytz import timezone

from rest_framework import viewsets, status
from django.http import JsonResponse
from rest_framework.decorators import action
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from rates.models import Rate
from rates.serializers import RateSerializer


class RateViewSet(viewsets.ModelViewSet):
    queryset = Rate.objects.all()
    serializer_class = RateSerializer
    http_method_names = ["get", "put", "head"]

    @classmethod
    def as_view(cls, actions=None, **initkwargs):
        view = super(RateViewSet, cls).as_view(actions, **initkwargs)

        def wrapped_view(*args, **kwargs):
            if args[0].method == "PUT":
                return cls().put(*args, **kwargs)
            return view(*args, **kwargs)

        return wrapped_view

    def put(self, request):
        data = JSONParser().parse(request)
        serializer = RateSerializer(data=data, many=True)

        if serializer.is_valid():
            Rate.objects.all().delete()
            serializer.save()

            return JsonResponse(
                serializer.data, status=status.HTTP_201_CREATED, safe=False
            )
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PriceView(APIView):
    def get(self, request):
        start_str = request.query_params.get("start")
        end_str = request.query_params.get("end")

        # Convert ISO-8601 strings to datetime objects
        start_dt = datetime.fromisoformat(start_str)
        end_dt = datetime.fromisoformat(end_str)

        # Check if the input spans more than one day
        if start_dt.date() != end_dt.date():
            return Response({"price": "unavailable"}, status=status.HTTP_200_OK)

        # TODO: Add logic to find the corresponding rate and calculate the price
        # For now return a placeholder response
        return Response({"price": 5000}, status=status.HTTP_200_OK)
