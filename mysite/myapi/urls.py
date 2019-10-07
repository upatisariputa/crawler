from django.urls import include, path
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register("main", views.MainViewSet, basename="main")
router.register("BJ", views.AllBjViewSet, basename="BJ")
router.register("afreeca_bj", views.ABjViewSet, base_name="afreeca_bj")
router.register("youtube_bj", views.YBjViewSet, base_name="youtube_bj")
router.register("twitch_bj", views.TBjViewSet, base_name="twitch_bj")

router.register("Video", views.AllVideolistViewSet, base_name="Video")
router.register("afreeca_Video", views.AVideolistViewSet,
                base_name="afreeca_Video")
router.register("youtube_Video", views.YVideolistViewSet,
                base_name="youtube_Video")
router.register("twitch_Video", views.TVideolistViewSet,
                base_name="twitch_Video")

router.register("Day", views.DayViewSet, base_name="Day")
router.register("Week", views.WeekViewSet, base_name="Week")
router.register("Month", views.MonthViewset, base_name="Month")

urlpatterns = [
    path("", include(router.urls)),
]
