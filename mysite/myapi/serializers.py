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
        fields = ["P_key", "P_url", "P_userkey", "P_name"]


class User_infoSerializer(serializers.ModelSerializer):
    Platform = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = User_info
        fields = ["U_key", "U_name", "U_img",
                  "U_info", "U_sudate", "P_key", "Platform"]


class SubSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscribe
        fields = ["S_key", "created_at", "S_count",
                  "year", "month", "week", "day", "P_key"]


class VideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Video
        fields = ["V_key", "V_name", "V_upload",
                  "like_A_Y", "dislike_Y", "view_A_Y_T", "comment_A_Y", "year", "month", "week", "day", "P_key"]


class TotalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Total
        fields = ["T_key", "T_like_count", "T_unlike_count",
                  "T_view_count", "T_update", "P_key"]


class D_sub_gapSerializer(serializers.ModelSerializer):
    class Meta:
        model = D_sub_gap
        fields = ["SD_key", "sub_count", "P_key"]


class W_sub_gapSerializer(serializers.ModelSerializer):
    class Meta:
        model = W_sub_gap
        fields = ["SW_key", "sub_count", "P_key"]


class M_sub_gapSerializer(serializers.ModelSerializer):
    class Meta:
        model = M_sub_gap
        fields = ["SM_key", "sub_count", "P_key"]


class D_video_gapSerializer(serializers.ModelSerializer):
    class Meta:
        model = D_video_gap
        fields = ["VD_key", "update", "like_count", "unlike_count",
                  "view_count", "comment_count"]


class W_video_gapSerializer(serializers.ModelSerializer):
    class Meta:
        model = W_video_gap
        fields = ["VW_key", "like_A_Y", "dislike_Y", "view_A_Y_T", "comment_A_Y", "P_key"
                  ]


class M_video_gapSerializer(serializers.ModelSerializer):
    class Meta:
        model = M_video_gap
        fields = ["VM_key", "like_A_Y", "dislike_Y",
                  "view_A_Y_T", "comment_A_Y", "P_key"]
