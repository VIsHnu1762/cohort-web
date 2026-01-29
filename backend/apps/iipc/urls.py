from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    LinkedInPostVerificationViewSet,
    LinkedInConnectionVerificationViewSet
)

router = DefaultRouter()
router.register(r'posts', LinkedInPostVerificationViewSet, basename='linkedin-post')
router.register(r'connections', LinkedInConnectionVerificationViewSet, basename='linkedin-connection')

urlpatterns = [
    path('', include(router.urls)),
]
