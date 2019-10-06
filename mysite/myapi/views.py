from .models import Total
from .models import User_info
from .models import Video
from .models import Subscribe
from .models import Platform
from .serializers import mainSerializer
from .serializers import bjSerializer
from .serializers import daySerializer
from .serializers import videolistSerializer
from .serializers import weekSerializer
from .serializers import monthSerializer

# from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response
from rest_framework import viewsets, views
from rest_framework.views import APIView
# from rest_framework.decorators import api_view
from django.http import Http404

import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "illio.settings")


class MainViewSet(viewsets.ModelViewSet):
    queryset = Platform.objects.all()
    serializer_class = mainSerializer


# class BjViewSet(viewsets.ModelViewSet):
#     @api_view(['GET', 'PUT', 'DELETE'])
#     def snippet_detail(request, pk):

#         # try:
#         #     snippet = Snippet.objects.get(pk=pk)
#         # except Snippet.DoesNotExist:
#         #     return Response(status=status.HTTP_404_NOT_FOUND)

#         # queryset = Platform.objects.filter(P_userkey=15620)
#         # serializer_class = bjSerializer


class VideolistViewSet(viewsets.ModelViewSet):
    queryset = Platform.objects.filter(P_name="afreeca")
    serializer_class = videolistSerializer


class DayViewSet(viewsets.ModelViewSet):
    queryset = Platform.objects.filter(P_name="afreeca")
    serializer_class = daySerializer


class WeekViewSet(viewsets.ModelViewSet):
    queryset = Platform.objects.all()
    serializer_class = weekSerializer


class MonthViewset(viewsets.ModelViewSet):
    queryset = Platform.objects.all()
    serializer_class = monthSerializer
