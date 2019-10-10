from .models import Total, User_info, Video, Subscribe, Platform
from .serializers import mainSerializer ,bjSerializer, daySerializer, videolistSerializer, weekSerializer, monthSerializer
from rest_framework import filters, generics, views, viewsets, permissions

from django_filters.rest_framework import DjangoFilterBackend
from django_filters import rest_framework as filters

from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import permissions

import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ilio.settings")
# class ProductList(generics.ListAPIView): 
#     queryset = Product.objects.all() 
#     serializer_class = ProductSerializer 
#     filter_backends = (DjangoFilterBackend,) 
#     filter_fields = ('category', 'in_stock')



class MainViewSet(viewsets.ModelViewSet):
    queryset = Platform.objects.all()
    serializer_class = mainSerializer
    permission_classes = [permissions.IsAdminUser]


# class AllBjViewSet(generics.ListAPIView):
#     queryset = Platform.objects.all()
#     serializer_class = bjSerializer
#     filter_fields = ('P_userkey','P_name')

class ProductList(generics.ListAPIView): 
    queryset = Platform.objects.all() 
    serializer_class = mainSerializer 
    filter_backends = (DjangoFilterBackend,) 
    filter_fields = ('P_userkey', 'P_name')


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
        groups = user.groups.reverse()[:7]
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
    lookup_field = 'P_userkey'
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
