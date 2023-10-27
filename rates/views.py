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

        if not start_str or not end_str:
            return Response(
                "query parameters, 'start' and 'end' are required to be specified as ISO-8601 strings.",
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Convert ISO-8601 strings to datetime objects
        start_dt_utc = datetime.fromisoformat(start_str).astimezone(timezone("UTC"))
        end_dt_utc = datetime.fromisoformat(end_str).astimezone(timezone("UTC"))

        # Check if the input spans more than one day
        if start_dt_utc.date() != end_dt_utc.date():
            return Response({"price": "unavailable"}, status=status.HTTP_200_OK)

        total_matches = 0
        price_match = None
        for rate in Rate.objects.all():
            rate_tz = timezone(rate.tz)
            start_dt = start_dt_utc.astimezone(rate_tz)
            end_dt = end_dt_utc.astimezone(rate_tz)

            # Check if the day of the week matches
            if start_dt.strftime("%a").lower() in rate.days.lower().split(","):
                rate_start_time, rate_end_time = map(int, rate.times.split("-"))

                # Check if the time range matches
                if (
                    rate_start_time <= int(start_dt.strftime("%H%M")) <= rate_end_time
                    and rate_start_time <= int(end_dt.strftime("%H%M")) <= rate_end_time
                ):
                    total_matches += 1
                    price_match = rate.price

                    # If rates overlap return default unavailable
                    if total_matches > 1:
                        return Response(
                            {"price": "unavailable"}, status=status.HTTP_200_OK
                        )

        if total_matches == 1:
            return Response({"price": price_match}, status=status.HTTP_200_OK)

        return Response({"price": "unavailable"}, status=status.HTTP_200_OK)
