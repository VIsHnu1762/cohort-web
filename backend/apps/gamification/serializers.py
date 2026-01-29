from rest_framework import serializers
from .models import (
    Season, Episode, EpisodeProgress, SeasonScore, LegacyScore,
    VaultWallet, VaultTransaction, SCDStreak, LeaderboardEntry,
    Title, UserTitle, PercentileBracket
)


class SeasonSerializer(serializers.ModelSerializer):
    is_current = serializers.ReadOnlyField()
    
    class Meta:
        model = Season
        fields = ['id', 'name', 'season_number', 'start_date', 'end_date', 
                  'is_active', 'is_current', 'created_at']


class EpisodeSerializer(serializers.ModelSerializer):
    required_pillars = serializers.SerializerMethodField()
    
    class Meta:
        model = Episode
        fields = ['id', 'season', 'episode_number', 'name', 'description',
                  'start_date', 'end_date', 'required_pillars']
    
    def get_required_pillars(self, obj):
        return obj.get_required_pillars()


class EpisodeProgressSerializer(serializers.ModelSerializer):
    episode_details = EpisodeSerializer(source='episode', read_only=True)
    completion_percentage = serializers.SerializerMethodField()
    
    class Meta:
        model = EpisodeProgress
        fields = ['id', 'student', 'episode', 'episode_details', 'status',
                  'clt_completed', 'cfc_task1_completed', 'cfc_task2_completed',
                  'cfc_task3_completed', 'iipc_task1_completed', 'iipc_task2_completed',
                  'sri_completed', 'scd_streak_active', 'started_at', 'completed_at',
                  'completion_percentage']
    
    def get_completion_percentage(self, obj):
        episode_num = obj.episode.episode_number
        completed_tasks = 0
        total_tasks = 0
        
        if episode_num == 1:
            total_tasks = 2
            completed_tasks = sum([obj.clt_completed, obj.scd_streak_active])
        elif episode_num == 2:
            total_tasks = 3
            completed_tasks = sum([obj.cfc_task1_completed, obj.iipc_task1_completed, obj.scd_streak_active])
        elif episode_num == 3:
            total_tasks = 3
            completed_tasks = sum([obj.cfc_task2_completed, obj.iipc_task2_completed, obj.scd_streak_active])
        elif episode_num == 4:
            total_tasks = 3
            completed_tasks = sum([obj.cfc_task3_completed, obj.sri_completed, obj.scd_streak_active])
        
        return (completed_tasks / total_tasks * 100) if total_tasks > 0 else 0


class SeasonScoreSerializer(serializers.ModelSerializer):
    season_name = serializers.CharField(source='season.name', read_only=True)
    breakdown = serializers.SerializerMethodField()
    
    class Meta:
        model = SeasonScore
        fields = ['id', 'student', 'season', 'season_name', 'clt_score', 'iipc_score',
                  'scd_score', 'cfc_score', 'outcome_score', 'total_score',
                  'season_completed', 'completed_at', 'breakdown', 'created_at']
    
    def get_breakdown(self, obj):
        return {
            'CLT': {'score': obj.clt_score, 'max': 100},
            'IIPC': {'score': obj.iipc_score, 'max': 200},
            'SCD': {'score': obj.scd_score, 'max': 100},
            'CFC': {'score': obj.cfc_score, 'max': 800},
            'Outcome': {'score': obj.outcome_score, 'max': 300},
        }


class LegacyScoreSerializer(serializers.ModelSerializer):
    student_name = serializers.CharField(source='student.username', read_only=True)
    average_season_score = serializers.SerializerMethodField()
    
    class Meta:
        model = LegacyScore
        fields = ['id', 'student', 'student_name', 'total_legacy_points',
                  'ascension_bonus_total', 'seasons_completed', 'highest_season_score',
                  'last_season_score', 'average_season_score', 'created_at', 'updated_at']
    
    def get_average_season_score(self, obj):
        if obj.seasons_completed > 0:
            return (obj.total_legacy_points - obj.ascension_bonus_total) / obj.seasons_completed
        return 0


class VaultTransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = VaultTransaction
        fields = ['id', 'transaction_type', 'amount', 'reason', 'created_at']


class VaultWalletSerializer(serializers.ModelSerializer):
    recent_transactions = serializers.SerializerMethodField()
    
    class Meta:
        model = VaultWallet
        fields = ['id', 'student', 'available_credits', 'total_earned',
                  'total_spent', 'recent_transactions', 'created_at', 'updated_at']
    
    def get_recent_transactions(self, obj):
        transactions = obj.transactions.all()[:10]
        return VaultTransactionSerializer(transactions, many=True).data


class SCDStreakSerializer(serializers.ModelSerializer):
    season_name = serializers.CharField(source='season.name', read_only=True)
    consistency_rating = serializers.SerializerMethodField()
    
    class Meta:
        model = SCDStreak
        fields = ['id', 'student', 'season', 'season_name', 'leetcode_username',
                  'current_streak', 'longest_streak', 'total_days_active',
                  'season_streak_days', 'streak_broken_count', 'streak_score',
                  'last_synced_at', 'consistency_rating']
    
    def get_consistency_rating(self, obj):
        if obj.streak_score >= 90:
            return 'Excellent'
        elif obj.streak_score >= 70:
            return 'Good'
        elif obj.streak_score >= 50:
            return 'Average'
        else:
            return 'Needs Improvement'


class LeaderboardEntrySerializer(serializers.ModelSerializer):
    student_name = serializers.SerializerMethodField()
    student_username = serializers.CharField(source='student.username', read_only=True)
    student_email = serializers.CharField(source='student.email', read_only=True)
    equipped_title = serializers.SerializerMethodField()
    
    class Meta:
        model = LeaderboardEntry
        fields = ['id', 'rank', 'student', 'student_name', 'student_username', 'student_email',
                  'season_score', 'rank_title', 'equipped_title', 'created_at']
    
    def get_student_name(self, obj):
        profile = getattr(obj.student, 'profile', None)
        if profile:
            return profile.full_name or obj.student.username
        return obj.student.username
    
    def get_equipped_title(self, obj):
        user_title = UserTitle.objects.filter(student=obj.student, is_equipped=True).first()
        if user_title:
            return user_title.title.name
        return None


class TitleSerializer(serializers.ModelSerializer):
    is_owned = serializers.SerializerMethodField()
    is_equipped = serializers.SerializerMethodField()
    
    class Meta:
        model = Title
        fields = ['id', 'name', 'description', 'vault_credit_cost', 'icon',
                  'rarity', 'is_active', 'is_owned', 'is_equipped']
    
    def get_is_owned(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return UserTitle.objects.filter(student=request.user, title=obj).exists()
        return False
    
    def get_is_equipped(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return UserTitle.objects.filter(
                student=request.user, title=obj, is_equipped=True
            ).exists()
        return False


class UserTitleSerializer(serializers.ModelSerializer):
    title_details = TitleSerializer(source='title', read_only=True)
    
    class Meta:
        model = UserTitle
        fields = ['id', 'student', 'title', 'title_details', 'is_equipped', 'unlocked_at']


class PercentileBracketSerializer(serializers.ModelSerializer):
    season_name = serializers.CharField(source='season.name', read_only=True)
    student_name = serializers.SerializerMethodField()
    student_username = serializers.CharField(source='student.username', read_only=True)
    
    class Meta:
        model = PercentileBracket
        fields = ['id', 'student', 'student_name', 'student_username', 'season', 
                  'season_name', 'percentile', 'season_score', 'created_at']
    
    def get_student_name(self, obj):
        profile = getattr(obj.student, 'profile', None)
        if profile:
            return profile.full_name or obj.student.username
        return obj.student.username


class StudentDashboardSerializer(serializers.Serializer):
    """Complete dashboard data for student"""
    current_season = SeasonSerializer()
    current_episode = EpisodeSerializer()
    episode_progress = EpisodeProgressSerializer()
    season_score = SeasonScoreSerializer()
    legacy_score = LegacyScoreSerializer()
    vault_wallet = VaultWalletSerializer()
    scd_streak = SCDStreakSerializer()
    leaderboard_position = serializers.CharField()
    percentile = PercentileBracketSerializer(allow_null=True)
    equipped_title = serializers.CharField(allow_null=True)
