from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    HackathonRegistrationViewSet,
    HackathonSubmissionViewSet,
    BMCVideoSubmissionViewSet,
    InternshipSubmissionViewSet,
    GenAIProjectSubmissionViewSet
)

router = DefaultRouter()
router.register(r'hackathon-registrations', HackathonRegistrationViewSet, basename='hackathon-registration')
router.register(r'hackathons', HackathonSubmissionViewSet, basename='hackathon')
router.register(r'bmc-videos', BMCVideoSubmissionViewSet, basename='bmc-video')
router.register(r'internships', InternshipSubmissionViewSet, basename='internship')
router.register(r'genai-projects', GenAIProjectSubmissionViewSet, basename='genai-project')

urlpatterns = [
    path('', include(router.urls)),
]
