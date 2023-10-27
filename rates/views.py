from rest_framework import viewsets, status
from django.http import JsonResponse
from rest_framework.parsers import JSONParser
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
