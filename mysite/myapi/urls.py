from django.urls import include, path
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register("main", views.MainViewSet, basename="main")
router.register("BJ", views.BjViewSet, basename="BJ")
router.register("Video", views.VideolistViewSet, base_name="Video")
router.register("Day", views.DayViewSet, base_name="Day")
router.register("Week", views.WeekViewSet, base_name="Week")
router.register("Month", views.MonthViewset, base_name="Month")

urlpatterns = [
    path("", include(router.urls))
    # path("main", views.MainViewSet, name="main")
]
