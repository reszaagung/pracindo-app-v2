# urls.py
from rest_framework.routers import DefaultRouter
from .views import GenerateStikerBesarViewSet

router = DefaultRouter()
router.register("generate-stiker", GenerateStikerBesarViewSet, basename="generate-stiker")
urlpatterns = router.urls