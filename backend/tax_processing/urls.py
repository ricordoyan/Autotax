from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    UserProfileViewSet,
    DependentViewSet,
    TaxDocumentViewSet,
    TaxReturnViewSet,
)

router = DefaultRouter()
router.register(r'profiles', UserProfileViewSet, basename='profile')
router.register(r'dependents', DependentViewSet, basename='dependent')
router.register(r'documents', TaxDocumentViewSet, basename='document')
router.register(r'tax-returns', TaxReturnViewSet, basename='tax-return')

app_name = 'tax_processing'

urlpatterns = [
    path('', include(router.urls)),
] 