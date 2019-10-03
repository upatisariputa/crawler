from .serializers import TotalSerializer
from .models import Total
from .serializers import User_infoSerializer
from .models import User_info
from .serializers import VideoSerializer
from .models import Video
from .serializers import SubSerializer
from .models import Subscribe
from .serializers import platformSerializer
from .models import Platform
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework.decorators import api_view
import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "illio.settings")


class MainViewSet(viewsets.ModelViewSet):
    print(Platform.objects.all())


# class BjViewSet(viewsets.ModelViewSet):

def Bj_info(request, userkey):
    if request.method == "POST":
        user = User_info.objects.filter(P_key=userkey)
        sub = Subscribe.objects.filter(P_key=userkey)
        youtube = Platform.objects.prefetch_related(
            "total").filter(P_key=userkey).get(P_name=youtube)
        twitch = Platform.objects.prefetch_related(
            "total").filter(P_key=userkey).get(P_name=youtube)
        afreeca = Platform.objects.prefetch_related(
            "total").filter(P_key=userkey).get(P_name=youtube)
        result = {"name": user.U_nmae,
                  "image": user.U_img,
                  "signup-date": user.U_suday,
                  "introduce": user.U_info,
                  "currnet_sub": {
                      "youtube": sub,
                      "twitch": sub,
                      "afreeca": sub
                  },
                  "youtube": {
                      "total_like": youtube.T_like,
                      "total_dislike": youtube.T_dislike,
                      "total_view": youtube.T_view
                  },
                  "twitch": {
                      "total_view": twitch.T_view
                  },
                  "afreeca": {
                      "total_like": afreeca.T_like,
                      "total_view": afreeca.T_view
                  }
                  }


class SubListViewSet(viewsets.ModelViewSet):
    queryset = Subscribe.objects.all().select_related("platform")
    serializer_class = SubSerializer


class BjListViewSet(viewsets.ModelViewSet):
    queryset = Platform.objects.all().select_related("Total")
    serializer_class = platformSerializer


class MaxLikeVideo(viewsets.ModelViewSet):
    queryset = Video.objects.all().order_by("like_count")
    serializer_class = VideoSerializer


class MinLikeVideo(viewsets.ModelViewSet):
    queryset = Video.objects.all().order_by("-like_count")
    serializer_class = VideoSerializer


class MaxViewCount(viewsets.ModelViewSet):
    queryset = Video.objects.all().order_by("view_count")
    serializer_class = VideoSerializer


class MinViewCount(viewsets.ModelViewSet):
    queryset = Video.objects.all().order_by("view_count")
    serializer_class = VideoSerializer
