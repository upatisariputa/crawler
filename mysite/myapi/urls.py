
from django.urls import include, path
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register("main", views.MainViewSet, basename="main")
router.register("BJ", views.BjViewSet, basename="BJ")
router.register("BJlist", views.BjListViewSet, basename="BJlist")
urlpatterns = [
    path("", include(router.urls))
    # path("main", views.MainViewSet, name="main")
]
