from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    SeasonViewSet, EpisodeViewSet, EpisodeProgressViewSet,
    SeasonScoreViewSet, LegacyScoreViewSet, VaultWalletViewSet,
    SCDStreakViewSet, LeaderboardViewSet, TitleViewSet,
    UserTitleViewSet, DashboardViewSet, ProgressNotificationViewSet
)
from . import mentor_views

router = DefaultRouter()
router.register(r'seasons', SeasonViewSet, basename='season')
router.register(r'episodes', EpisodeViewSet, basename='episode')
router.register(r'episode-progress', EpisodeProgressViewSet, basename='episode-progress')
router.register(r'season-scores', SeasonScoreViewSet, basename='season-score')
router.register(r'legacy-scores', LegacyScoreViewSet, basename='legacy-score')
router.register(r'vault-wallets', VaultWalletViewSet, basename='vault-wallet')
router.register(r'scd-streaks', SCDStreakViewSet, basename='scd-streak')
router.register(r'leaderboard', LeaderboardViewSet, basename='leaderboard')
router.register(r'titles', TitleViewSet, basename='title')
router.register(r'user-titles', UserTitleViewSet, basename='user-title')
router.register(r'dashboard', DashboardViewSet, basename='dashboard')
router.register(r'progress-notifications', ProgressNotificationViewSet, basename='progress-notification')

urlpatterns = [
    path('', include(router.urls)),
    
    # Mentor-only endpoints
    path('mentor/approve-task/', mentor_views.approve_task, name='mentor-approve-task'),
    path('mentor/student-progress/<int:student_id>/', mentor_views.student_progress_detail, name='mentor-student-progress'),
    path('mentor/finalize-season/<int:student_id>/', mentor_views.finalize_student_season, name='mentor-finalize-season'),
]
