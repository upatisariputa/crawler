from rest_framework import serializers
from .models import Platform
from .models import User_info
from .models import Subscribe
from .models import Video
from .models import Total
from .models import D_sub_gap
from .models import W_sub_gap
from .models import M_sub_gap
from .models import D_video_gap
from .models import W_video_gap
from .models import M_video_gap


class platformSerializer(serializers.ModelSerializer):
    class Meta:
        model = Platform
        fields = ("id", "name", "type", "url")


class User_infoSerializer(serializers.ModelSerializer):
    class Meta:
        model = User_info
        fields = ("id", "U_img", "U_introduce", "U_singup_day", "platform")


class SubSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscribe
        fields = ("id", "update", "count", "platform")


class VideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Video
        fields = ("id", "like_count", "unlike_count",
                  "view_count", "comment_count", "platform")


class TotalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Total
        fields = ("id", "t_like_count", "t_unlike_count",
                  "t_view_count", "platform")


class D_sub_gapSerializer(serializers.ModelSerializer):
    class Meta:
        model = D_sub_gap
        fields = ("id", "update", "count")


class W_sub_gapSerializer(serializers.ModelSerializer):
    class Meta:
        model = W_sub_gap
        fields = ("id", "update", "count")


class M_sub_gapSerializer(serializers.ModelSerializer):
    class Meta:
        model = M_sub_gap
        fields = ("id", "update", "count")


class D_video_gapSerializer(serializers.ModelSerializer):
    class Meta:
        model = D_video_gap
        fields = ("id", "update", "like_count", "unlike_count",
                  "view_count", "comment_count")


class W_video_gapSerializer(serializers.ModelSerializer):
    class Meta:
        model = W_video_gap
        fields = ("id", "update", "like_count", "unlike_count",
                  "view_count", "comment_count")


class M_video_gapSerializer(serializers.ModelSerializer):
    class Meta:
        model = M_video_gap
        fields = ("id", "update", "like_count", "unlike_count",
                  "view_count", "comment_count")
