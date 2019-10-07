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

from rest_framework.decorators import action
# from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response
from rest_framework import viewsets, views
from rest_framework.views import APIView
# from rest_framework.decorators import api_view
from django.http import Http404
from rest_framework import permissions

import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ilio.settings")


class MainViewSet(viewsets.ModelViewSet):
    queryset = Platform.objects.all()
    serializer_class = mainSerializer
    permission_classes = [permissions.IsAdminUser]


class AllBjViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Platform.objects.all()
    serializer_class = bjSerializer
    lookup_field = 'P_userkey'
    permission_classes = [permissions.IsAdminUser]

    @action(detail=True)
    def group_names(self, request, pk=None):
        user = self.get_object()
        groups = user.groups.all()
        return Response([group.name for group in groups])


class ABjViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Platform.objects.filter(P_name="afreeca")
    serializer_class = bjSerializer
    lookup_field = 'P_userkey'
    permission_classes = [permissions.IsAdminUser]

    @action(detail=True)
    def group_names(self, request, pk=None):
        user = self.get_object()
        groups = user.groups.all()
        return Response([group.name for group in groups])


class YBjViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Platform.objects.filter(P_name="youtube")
    serializer_class = bjSerializer
    lookup_field = 'P_userkey'
    permission_classes = [permissions.IsAdminUser]

    @action(detail=True)
    def group_names(self, request, pk=None):
        user = self.get_object()
        groups = user.groups.all()
        return Response([group.name for group in groups])


class TBjViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Platform.objects.filter(P_name="twitch")
    serializer_class = bjSerializer
    lookup_field = 'P_userkey'
    permission_classes = [permissions.IsAdminUser]

    @action(detail=True)
    def group_names(self, request, pk=None):
        user = self.get_object()
        groups = user.groups.all()
        return Response([group.name for group in groups])


class AllVideolistViewSet(viewsets.ModelViewSet):
    queryset = Platform.objects.all()
    serializer_class = videolistSerializer
    lookup_field = 'P_userkey'
    permission_classes = [permissions.IsAdminUser]

    @action(detail=True)
    def group_names(self, request, pk=None):
        user = self.get_object()
        groups = user.groups.all()
        return Response([group.name for group in groups])


class AVideolistViewSet(viewsets.ModelViewSet):
    queryset = Platform.objects.filter(P_name="afreeca")
    serializer_class = videolistSerializer
    lookup_field = 'P_userkey'
    permission_classes = [permissions.IsAdminUser]

    @action(detail=True)
    def group_names(self, request, pk=None):
        user = self.get_object()
        groups = user.groups.all()
        return Response([group.name for group in groups])


class YVideolistViewSet(viewsets.ModelViewSet):
    queryset = Platform.objects.filter(P_name="youtube")
    serializer_class = videolistSerializer
    lookup_field = 'P_userkey'
    permission_classes = [permissions.IsAdminUser]

    @action(detail=True)
    def group_names(self, request, pk=None):
        user = self.get_object()
        groups = user.groups.all()
        return Response([group.name for group in groups])


class TVideolistViewSet(viewsets.ModelViewSet):
    queryset = Platform.objects.filter(P_name="twitch")
    serializer_class = videolistSerializer
    lookup_field = 'P_userkey'
    permission_classes = [permissions.IsAdminUser]

    @action(detail=True)
    def group_names(self, request, pk=None):
        user = self.get_object()
        groups = user.groups.all()
        return Response([group.name for group in groups])


class DayViewSet(viewsets.ModelViewSet):
    queryset = Platform.objects.all()
    serializer_class = daySerializer
    lookup_field = 'P_name'
    permission_classes = [permissions.IsAdminUser]

    @action(detail=True)
    def group_names(self, request, pk=None):
        user = self.get_object()
        groups = user.groups.all()
        return Response([group.name for group in groups])


class WeekViewSet(viewsets.ModelViewSet):
    queryset = Platform.objects.all()
    serializer_class = weekSerializer
    lookup_field = 'P_name'
    permission_classes = [permissions.IsAdminUser]

    @action(detail=True)
    def group_names(self, request, pk=None):
        user = self.get_object()
        groups = user.groups.all()
        return Response([group.name for group in groups])


class MonthViewset(viewsets.ModelViewSet):
    queryset = Platform.objects.all()
    serializer_class = monthSerializer
    lookup_field = 'P_name'
    permission_classes = [permissions.IsAdminUser]

    @action(detail=True)
    def group_names(self, request, pk=None):
        user = self.get_object()
        groups = user.groups.all()
        return Response([group.name for group in groups])
