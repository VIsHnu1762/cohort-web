from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import LeetCodeProfileViewSet

router = DefaultRouter()
router.register(r'profiles', LeetCodeProfileViewSet, basename='leetcode-profile')

urlpatterns = [
    path('', include(router.urls)),
]
