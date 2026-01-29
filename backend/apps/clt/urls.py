from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CLTSubmissionViewSet

router = DefaultRouter()
router.register(r'submissions', CLTSubmissionViewSet, basename='clt-submission')

urlpatterns = [
    path('', include(router.urls)),
]
