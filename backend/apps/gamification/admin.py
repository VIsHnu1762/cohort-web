from django.contrib import admin
from .models import (
    Season, Episode, EpisodeProgress, SeasonScore, LegacyScore,
    VaultWallet, VaultTransaction, SCDStreak, LeaderboardEntry,
    Title, UserTitle, PercentileBracket
)


@admin.register(Season)
class SeasonAdmin(admin.ModelAdmin):
    list_display = ['name', 'season_number', 'start_date', 'end_date', 'is_active', 'is_current']
    list_filter = ['is_active', 'start_date']
    search_fields = ['name']


@admin.register(Episode)
class EpisodeAdmin(admin.ModelAdmin):
    list_display = ['episode_number', 'season', 'name', 'start_date', 'end_date']
    list_filter = ['season', 'episode_number']
    search_fields = ['name']


@admin.register(EpisodeProgress)
class EpisodeProgressAdmin(admin.ModelAdmin):
    list_display = ['student', 'episode', 'status', 'started_at', 'completed_at']
    list_filter = ['status', 'episode__season', 'episode__episode_number']
    search_fields = ['student__username', 'student__email']
    readonly_fields = ['started_at', 'completed_at']


@admin.register(SeasonScore)
class SeasonScoreAdmin(admin.ModelAdmin):
    list_display = ['student', 'season', 'total_score', 'season_completed', 'completed_at']
    list_filter = ['season_completed', 'season']
    search_fields = ['student__username']
    readonly_fields = ['total_score', 'completed_at']


@admin.register(LegacyScore)
class LegacyScoreAdmin(admin.ModelAdmin):
    list_display = ['student', 'total_legacy_points', 'seasons_completed', 'ascension_bonus_total']
    search_fields = ['student__username']
    readonly_fields = ['created_at', 'updated_at']


@admin.register(VaultWallet)
class VaultWalletAdmin(admin.ModelAdmin):
    list_display = ['student', 'available_credits', 'total_earned', 'total_spent']
    search_fields = ['student__username']
    readonly_fields = ['created_at', 'updated_at']


@admin.register(VaultTransaction)
class VaultTransactionAdmin(admin.ModelAdmin):
    list_display = ['wallet', 'transaction_type', 'amount', 'reason', 'created_at']
    list_filter = ['transaction_type', 'created_at']
    search_fields = ['wallet__student__username', 'reason']


@admin.register(SCDStreak)
class SCDStreakAdmin(admin.ModelAdmin):
    list_display = ['student', 'season', 'current_streak', 'season_streak_days', 'streak_score']
    list_filter = ['season']
    search_fields = ['student__username', 'leetcode_username']


@admin.register(LeaderboardEntry)
class LeaderboardEntryAdmin(admin.ModelAdmin):
    list_display = ['rank', 'student', 'season', 'season_score', 'rank_title']
    list_filter = ['season', 'rank']
    search_fields = ['student__username']


@admin.register(Title)
class TitleAdmin(admin.ModelAdmin):
    list_display = ['name', 'rarity', 'vault_credit_cost', 'is_active']
    list_filter = ['rarity', 'is_active']
    search_fields = ['name']


@admin.register(UserTitle)
class UserTitleAdmin(admin.ModelAdmin):
    list_display = ['student', 'title', 'is_equipped', 'unlocked_at']
    list_filter = ['is_equipped', 'title']
    search_fields = ['student__username']


@admin.register(PercentileBracket)
class PercentileBracketAdmin(admin.ModelAdmin):
    list_display = ['student', 'season', 'percentile', 'season_score']
    list_filter = ['season', 'percentile']
    search_fields = ['student__username']
