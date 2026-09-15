from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import GenerateStikerBesarViewSet, GenerateStikerKecil12ViewSet, TemplateStikerKecil12ViewSet

app_name = 'fitur'  

router = DefaultRouter()
router.register(r"generate-stiker", GenerateStikerBesarViewSet, basename="generate-stiker")
router.register(r"generate-stiker-kecil-12", GenerateStikerKecil12ViewSet, basename="generate-stiker-kecil-12")
router.register(r"template-stiker-kecil-12", TemplateStikerKecil12ViewSet, basename="template-stiker-kecil-12")

urlpatterns = [
    path('', include(router.urls)),
]