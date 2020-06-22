from rest_framework.routers import DefaultRouter
from .views import TrendViewSet


router = DefaultRouter()

router.register(r'trends', TrendViewSet)

urlpatterns = router.urls