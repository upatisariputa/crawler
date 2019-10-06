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

from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework import permissions
import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "illio.settings")


class MainViewSet(viewsets.ModelViewSet):
    queryset = Platform.objects.all()
    serializer_class = mainSerializer
    permission_classes = [permissions.IsAdminUser]


class BjViewSet(viewsets.ModelViewSet):
    queryset = Platform.objects.all()
    serializer_class = bjSerializer
    permission_classes = [permissions.IsAdminUser]


class VideolistViewSet(viewsets.ModelViewSet):
    queryset = Platform.objects.all()
    serializer_class = videolistSerializer
    permission_classes = [permissions.IsAdminUser]


class DayViewSet(viewsets.ModelViewSet):
    queryset = Platform.objects.all()
    serializer_class = daySerializer
    permission_classes = [permissions.IsAdminUser]


class WeekViewSet(viewsets.ModelViewSet):
    queryset = Platform.objects.all()
    serializer_class = weekSerializer
    permission_classes = [permissions.IsAdminUser]


class MonthViewset(viewsets.ModelViewSet):
    queryset = Platform.objects.all()
    serializer_class = monthSerializer
    permission_classes = [permissions.IsAdminUser]
