from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from django.utils import timezone

from .models import (
    Season, Episode, EpisodeProgress, SeasonScore, LegacyScore,
    VaultWallet, SCDStreak, LeaderboardEntry, Title, UserTitle,
    PercentileBracket
)
from .serializers import (
    SeasonSerializer, EpisodeSerializer, EpisodeProgressSerializer,
    SeasonScoreSerializer, LegacyScoreSerializer, VaultWalletSerializer,
    SCDStreakSerializer, LeaderboardEntrySerializer, TitleSerializer,
    UserTitleSerializer, PercentileBracketSerializer, StudentDashboardSerializer
)
from .services import EpisodeService, TitleService, LeetCodeSyncService
from .progress_notifications import ProgressNotificationService


class SeasonViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Read-only viewset for seasons
    Students can view season information
    """
    queryset = Season.objects.all()
    serializer_class = SeasonSerializer
    permission_classes = [IsAuthenticated]
    
    @action(detail=False, methods=['get'])
    def current(self, request):
        """Get current active season"""
        current_season = Season.objects.filter(
            is_active=True,
            start_date__lte=timezone.now().date(),
            end_date__gte=timezone.now().date()
        ).first()
        
        if current_season:
            serializer = self.get_serializer(current_season)
            return Response(serializer.data)
        return Response({'detail': 'No active season'}, status=status.HTTP_404_NOT_FOUND)


class EpisodeViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Read-only viewset for episodes
    """
    queryset = Episode.objects.all()
    serializer_class = EpisodeSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        queryset = super().get_queryset()
        season_id = self.request.query_params.get('season')
        if season_id:
            queryset = queryset.filter(season_id=season_id)
        return queryset


class EpisodeProgressViewSet(viewsets.ModelViewSet):
    """
    Student can view and update their episode progress
    """
    serializer_class = EpisodeProgressSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return EpisodeProgress.objects.filter(student=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(student=self.request.user)
    
    @action(detail=False, methods=['get'])
    def current(self, request):
        """Get current episode progress"""
        current_season = Season.objects.filter(is_active=True).first()
        if not current_season:
            return Response({'detail': 'No active season'}, status=status.HTTP_404_NOT_FOUND)
        
        current_episode = EpisodeService.get_current_episode(request.user, current_season)
        if not current_episode:
            return Response({'detail': 'No active episode'}, status=status.HTTP_404_NOT_FOUND)
        
        progress = EpisodeProgress.objects.filter(
            student=request.user,
            episode=current_episode
        ).first()
        
        if progress:
            serializer = self.get_serializer(progress)
            return Response(serializer.data)
        return Response({'detail': 'Progress not found'}, status=status.HTTP_404_NOT_FOUND)


class SeasonScoreViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Student can view their season scores
    """
    serializer_class = SeasonScoreSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return SeasonScore.objects.filter(student=self.request.user)
    
    @action(detail=False, methods=['get'])
    def current(self, request):
        """Get current season score"""
        current_season = Season.objects.filter(is_active=True).first()
        if not current_season:
            return Response({'detail': 'No active season'}, status=status.HTTP_404_NOT_FOUND)
        
        score, created = SeasonScore.objects.get_or_create(
            student=request.user,
            season=current_season
        )
        
        serializer = self.get_serializer(score)
        return Response(serializer.data)


class LegacyScoreViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Student can view their legacy score
    """
    serializer_class = LegacyScoreSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return LegacyScore.objects.filter(student=self.request.user)
    
    @action(detail=False, methods=['get'])
    def my_score(self, request):
        """Get authenticated user's legacy score"""
        score, created = LegacyScore.objects.get_or_create(student=request.user)
        serializer = self.get_serializer(score)
        return Response(serializer.data)


class VaultWalletViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Student can view their vault wallet
    """
    serializer_class = VaultWalletSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return VaultWallet.objects.filter(student=self.request.user)
    
    @action(detail=False, methods=['get'])
    def my_wallet(self, request):
        """Get authenticated user's wallet"""
        wallet, created = VaultWallet.objects.get_or_create(student=request.user)
        serializer = self.get_serializer(wallet)
        return Response(serializer.data)


class SCDStreakViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Student can view their SCD streak
    """
    serializer_class = SCDStreakSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return SCDStreak.objects.filter(student=self.request.user)
    
    @action(detail=False, methods=['get'])
    def current(self, request):
        """Get current season streak"""
        current_season = Season.objects.filter(is_active=True).first()
        if not current_season:
            return Response({'detail': 'No active season'}, status=status.HTTP_404_NOT_FOUND)
        
        streak, created = SCDStreak.objects.get_or_create(
            student=request.user,
            season=current_season
        )
        
        serializer = self.get_serializer(streak)
        return Response(serializer.data)
    
    @action(detail=False, methods=['post'])
    def sync(self, request):
        """Manually trigger streak sync"""
        current_season = Season.objects.filter(is_active=True).first()
        if not current_season:
            return Response({'detail': 'No active season'}, status=status.HTTP_404_NOT_FOUND)
        
        streak, message = LeetCodeSyncService.sync_student_streak(request.user, current_season)
        
        if streak:
            serializer = self.get_serializer(streak)
            return Response({
                'message': message,
                'streak': serializer.data
            })
        return Response({'error': message}, status=status.HTTP_400_BAD_REQUEST)


class LeaderboardViewSet(viewsets.ReadOnlyModelViewSet):
    """
    View Champions Podium (Top 3 only)
    """
    serializer_class = LeaderboardEntrySerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        season_id = self.request.query_params.get('season')
        queryset = LeaderboardEntry.objects.all()
        if season_id:
            queryset = queryset.filter(season_id=season_id)
        return queryset
    
    @action(detail=False, methods=['get'])
    def current_season(self, request):
        """Get current season's top 3 (for students)"""
        current_season = Season.objects.filter(is_active=True).first()
        if not current_season:
            return Response({'detail': 'No active season'}, status=status.HTTP_404_NOT_FOUND)
        
        top_3 = LeaderboardEntry.objects.filter(season=current_season).order_by('rank')
        serializer = self.get_serializer(top_3, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def full_leaderboard(self, request):
        """Get full leaderboard (for mentors and floor wings)"""
        current_season = Season.objects.filter(is_active=True).first()
        if not current_season:
            return Response({'detail': 'No active season'}, status=status.HTTP_404_NOT_FOUND)
        
        # Get all leaderboard entries for current season
        all_entries = LeaderboardEntry.objects.filter(season=current_season).order_by('rank')
        
        # Get all percentile brackets
        percentiles = PercentileBracket.objects.filter(season=current_season).order_by('-season_score')
        
        leaderboard_data = self.get_serializer(all_entries, many=True).data
        
        # Add percentile data
        from .serializers import PercentileBracketSerializer
        percentile_data = PercentileBracketSerializer(percentiles, many=True).data
        
        return Response({
            'top_ranks': leaderboard_data,
            'percentiles': percentile_data,
            'total_students': len(leaderboard_data) + len(percentile_data)
        })
    
    @action(detail=False, methods=['get'])
    def my_position(self, request):
        """Get user's position (rank or percentile)"""
        current_season = Season.objects.filter(is_active=True).first()
        if not current_season:
            return Response({'detail': 'No active season'}, status=status.HTTP_404_NOT_FOUND)
        
        # Check if in top 3
        leaderboard_entry = LeaderboardEntry.objects.filter(
            season=current_season,
            student=request.user
        ).first()
        
        if leaderboard_entry:
            return Response({
                'position_type': 'leaderboard',
                'rank': leaderboard_entry.rank,
                'rank_title': leaderboard_entry.rank_title,
                'season_score': leaderboard_entry.season_score
            })
        
        # Check percentile
        percentile = PercentileBracket.objects.filter(
            season=current_season,
            student=request.user
        ).first()
        
        if percentile:
            return Response({
                'position_type': 'percentile',
                'percentile': percentile.get_percentile_display(),
                'season_score': percentile.season_score
            })
        
        # Not completed season
        return Response({
            'position_type': 'not_completed',
            'message': 'Complete all 4 episodes to be ranked'
        })


class TitleViewSet(viewsets.ReadOnlyModelViewSet):
    """
    View available titles
    """
    serializer_class = TitleSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return Title.objects.filter(is_active=True)
    
    @action(detail=True, methods=['post'])
    def redeem(self, request, pk=None):
        """Redeem a title using Vault Credits"""
        title = self.get_object()
        success, message = TitleService.redeem_title(request.user, title)
        
        if success:
            return Response({'message': message}, status=status.HTTP_200_OK)
        return Response({'error': message}, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=True, methods=['post'])
    def equip(self, request, pk=None):
        """Equip a title"""
        title = self.get_object()
        success, message = TitleService.equip_title(request.user, title)
        
        if success:
            return Response({'message': message}, status=status.HTTP_200_OK)
        return Response({'error': message}, status=status.HTTP_400_BAD_REQUEST)


class UserTitleViewSet(viewsets.ModelViewSet):
    """
    View and equip owned titles
    """
    serializer_class = UserTitleSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return UserTitle.objects.filter(student=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(student=self.request.user)
    
    @action(detail=True, methods=['post'])
    def equip(self, request, pk=None):
        """Equip a title"""
        user_title = self.get_object()
        # Unequip all other titles
        UserTitle.objects.filter(student=request.user, is_equipped=True).update(is_equipped=False)
        # Equip this title
        user_title.is_equipped = True
        user_title.save()
        serializer = self.get_serializer(user_title)
        return Response(serializer.data)


class DashboardViewSet(viewsets.ViewSet):
    """
    Complete gamification dashboard for students
    """
    permission_classes = [IsAuthenticated]
    
    @action(detail=False, methods=['get'])
    def student_overview(self, request):
        """Get complete gamification overview for student"""
        user = request.user
        
        # Get current season
        current_season = Season.objects.filter(is_active=True).first()
        if not current_season:
            return Response({'detail': 'No active season'}, status=status.HTTP_404_NOT_FOUND)
        
        # Get current episode
        current_episode = EpisodeService.get_current_episode(user, current_season)
        
        # Get progress
        episode_progress = None
        if current_episode:
            episode_progress = EpisodeProgress.objects.filter(
                student=user,
                episode=current_episode
            ).first()
        
        # Get scores
        season_score, _ = SeasonScore.objects.get_or_create(student=user, season=current_season)
        legacy_score, _ = LegacyScore.objects.get_or_create(student=user)
        vault_wallet, _ = VaultWallet.objects.get_or_create(student=user)
        scd_streak, _ = SCDStreak.objects.get_or_create(student=user, season=current_season)
        
        # Get leaderboard position
        leaderboard_entry = LeaderboardEntry.objects.filter(
            season=current_season,
            student=user
        ).first()
        
        percentile = PercentileBracket.objects.filter(
            season=current_season,
            student=user
        ).first()
        
        leaderboard_position = "Not Ranked"
        if leaderboard_entry:
            leaderboard_position = f"Rank {leaderboard_entry.rank} - {leaderboard_entry.rank_title}"
        elif percentile:
            leaderboard_position = percentile.get_percentile_display()
        
        # Get equipped title
        equipped_title_obj = UserTitle.objects.filter(student=user, is_equipped=True).first()
        equipped_title = equipped_title_obj.title.name if equipped_title_obj else None
        
        # Compile dashboard data
        dashboard_data = {
            'current_season': SeasonSerializer(current_season).data,
            'current_episode': EpisodeSerializer(current_episode).data if current_episode else None,
            'episode_progress': EpisodeProgressSerializer(episode_progress).data if episode_progress else None,
            'season_score': SeasonScoreSerializer(season_score).data,
            'legacy_score': LegacyScoreSerializer(legacy_score).data,
            'vault_wallet': VaultWalletSerializer(vault_wallet).data,
            'scd_streak': SCDStreakSerializer(scd_streak).data,
            'leaderboard_position': leaderboard_position,
            'percentile': PercentileBracketSerializer(percentile).data if percentile else None,
            'equipped_title': equipped_title,
        }
        
        return Response(dashboard_data)


class ProgressNotificationViewSet(viewsets.ViewSet):
    """
    ViewSet for progress notifications and batch statistics
    """
    permission_classes = [IsAuthenticated]
    
    @action(detail=False, methods=['get'])
    def batch_stats(self, request):
        """Get batch-wide statistics"""
        stats = ProgressNotificationService.get_batch_statistics()
        
        if not stats:
            return Response(
                {'detail': 'No active season found'},
                status=status.HTTP_404_NOT_FOUND
            )
        
        return Response(stats)
    
    @action(detail=False, methods=['get'])
    def my_comparison(self, request):
        """Get student's progress comparison with batch average"""
        comparison = ProgressNotificationService.get_student_comparison(request.user)
        
        if not comparison:
            return Response(
                {'detail': 'Unable to generate comparison'},
                status=status.HTTP_404_NOT_FOUND
            )
        
        return Response(comparison)
