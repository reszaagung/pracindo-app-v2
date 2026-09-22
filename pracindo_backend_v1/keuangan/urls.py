from django.urls import include, path

from rest_framework.routers import DefaultRouter

from .views import (
    MonitoringKasAPIView,
    MonitoringKeuanganAPIView,
    MonitoringTagihanAPIView,
    PengeluaranViewSet,
)


app_name = "keuangan"


router = DefaultRouter()

router.register(
    r"pengeluaran",
    PengeluaranViewSet,
    basename="pengeluaran",
)


urlpatterns = [
    path(
        "",
        include(router.urls),
    ),

    path(
        "monitoring/",
        MonitoringKeuanganAPIView.as_view(),
        name="monitoring",
    ),

    path(
        "monitoring/tagihan/",
        MonitoringTagihanAPIView.as_view(),
        name="monitoring-tagihan",
    ),

    path(
        "monitoring/kas/",
        MonitoringKasAPIView.as_view(),
        name="monitoring-kas",
    ),
]