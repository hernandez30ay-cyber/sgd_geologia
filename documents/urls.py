from rest_framework.routers import DefaultRouter
from .views import DocumentViewSet, DocumentMetadataViewSet

router = DefaultRouter()
router.register(r"", DocumentViewSet, basename="documents")
router.register(r"metadata", DocumentMetadataViewSet, basename="metadata")

urlpatterns = router.urls
