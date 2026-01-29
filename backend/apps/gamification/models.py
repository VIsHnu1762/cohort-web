from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone
from datetime import datetime, timedelta

User = get_user_model()


class Season(models.Model):
    """
    One Month = One Season
    Contains 4 Episodes (weekly)
    """
    name = models.CharField(max_length=100)  # e.g., "Season 1 - January 2025"
    season_number = models.PositiveIntegerField()
    start_date = models.DateField()
    end_date = models.DateField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-season_number']
        unique_together = ['season_number']

    def __str__(self):
        return f"{self.name} (Season {self.season_number})"

    @property
    def is_current(self):
        today = timezone.now().date()
        return self.start_date <= today <= self.end_date


class Episode(models.Model):
    """
    4 Episodes per Season (weekly)
    Episode N unlocks only after Episode N-1 is completed
    """
    EPISODE_CHOICES = [
        (1, 'Episode 1 - Kickoff'),
        (2, 'Episode 2 - Build'),
        (3, 'Episode 3 - Intensity'),
        (4, 'Episode 4 - Finale'),
    ]

    season = models.ForeignKey(Season, on_delete=models.CASCADE, related_name='episodes')
    episode_number = models.PositiveIntegerField(choices=EPISODE_CHOICES)
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    start_date = models.DateField()
    end_date = models.DateField()

    class Meta:
        ordering = ['season', 'episode_number']
        unique_together = ['season', 'episode_number']

    def __str__(self):
        return f"{self.season.name} - Episode {self.episode_number}"

    def get_required_pillars(self):
        """Returns pillars required for this episode"""
        requirements = {
            1: ['CLT', 'SCD'],  # Kickoff
            2: ['CFC', 'IIPC', 'SCD'],  # Build
            3: ['CFC', 'IIPC', 'SCD'],  # Intensity
            4: ['CFC', 'SRI', 'SCD'],  # Finale
        }
        return requirements.get(self.episode_number, [])


class EpisodeProgress(models.Model):
    """
    Tracks student progress through episodes
    Episode unlocks only after previous episode completion
    """
    STATUS_CHOICES = [
        ('locked', 'Locked'),
        ('unlocked', 'Unlocked'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
    ]

    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='episode_progress')
    episode = models.ForeignKey(Episode, on_delete=models.CASCADE, related_name='student_progress')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='locked')
    
    # Task completion tracking
    clt_completed = models.BooleanField(default=False)
    cfc_task1_completed = models.BooleanField(default=False)
    cfc_task2_completed = models.BooleanField(default=False)
    cfc_task3_completed = models.BooleanField(default=False)
    iipc_task1_completed = models.BooleanField(default=False)
    iipc_task2_completed = models.BooleanField(default=False)
    sri_completed = models.BooleanField(default=False)
    scd_streak_active = models.BooleanField(default=False)
    
    started_at = models.DateTimeField(null=True, blank=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        unique_together = ['student', 'episode']
        ordering = ['episode__season', 'episode__episode_number']

    def __str__(self):
        return f"{self.student.username} - {self.episode}"

    def check_episode_completion(self):
        """Check if all required tasks for this episode are completed"""
        episode_num = self.episode.episode_number
        
        if episode_num == 1:
            return self.clt_completed and self.scd_streak_active
        elif episode_num == 2:
            return self.cfc_task1_completed and self.iipc_task1_completed and self.scd_streak_active
        elif episode_num == 3:
            return self.cfc_task2_completed and self.iipc_task2_completed and self.scd_streak_active
        elif episode_num == 4:
            return self.cfc_task3_completed and self.sri_completed and self.scd_streak_active
        return False

    def mark_completed(self):
        """Mark episode as completed and unlock next episode"""
        if self.status != 'completed' and self.check_episode_completion():
            self.status = 'completed'
            self.completed_at = timezone.now()
            self.save()
            
            # Unlock next episode
            next_episode = Episode.objects.filter(
                season=self.episode.season,
                episode_number=self.episode.episode_number + 1
            ).first()
            
            if next_episode:
                EpisodeProgress.objects.update_or_create(
                    student=self.student,
                    episode=next_episode,
                    defaults={'status': 'unlocked'}
                )
            
            # Check if season is complete (all 4 episodes done)
            if self.episode.episode_number == 4:
                self._check_season_completion()
    
    def _check_season_completion(self):
        """Check if all episodes in season are completed"""
        from apps.gamification.services import SeasonScoringService
        
        all_completed = EpisodeProgress.objects.filter(
            student=self.student,
            episode__season=self.episode.season,
            status='completed'
        ).count() == 4
        
        if all_completed:
            # Trigger season finalization
            SeasonScoringService.finalize_season(self.student, self.episode.season)


class SeasonScore(models.Model):
    """
    1500 Point System - Calculated ONLY after full Season completion
    """
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='season_scores')
    season = models.ForeignKey(Season, on_delete=models.CASCADE, related_name='student_scores')
    
    # Pillar-wise breakdown (1500 total)
    clt_score = models.PositiveIntegerField(default=0, validators=[MaxValueValidator(100)])  # 100 max
    iipc_score = models.PositiveIntegerField(default=0, validators=[MaxValueValidator(200)])  # 200 max
    scd_score = models.PositiveIntegerField(default=0, validators=[MaxValueValidator(100)])  # 100 max
    cfc_score = models.PositiveIntegerField(default=0, validators=[MaxValueValidator(800)])  # 800 max
    outcome_score = models.PositiveIntegerField(default=0, validators=[MaxValueValidator(300)])  # 300 max
    
    total_score = models.PositiveIntegerField(default=0, validators=[MaxValueValidator(1500)])
    
    # Completion status
    season_completed = models.BooleanField(default=False)
    completed_at = models.DateTimeField(null=True, blank=True)
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ['student', 'season']
        ordering = ['-season__season_number']

    def __str__(self):
        return f"{self.student.username} - {self.season.name} - {self.total_score}/1500"

    def calculate_total(self):
        """Calculate total season score"""
        self.total_score = (
            self.clt_score + 
            self.iipc_score + 
            self.scd_score + 
            self.cfc_score + 
            self.outcome_score
        )
        self.save()
        return self.total_score


class LegacyScore(models.Model):
    """
    Lifetime cumulative score - Never resets
    Includes Season Scores + Ascension Bonus + Special achievements
    """
    student = models.OneToOneField(User, on_delete=models.CASCADE, related_name='legacy_score')
    total_legacy_points = models.PositiveIntegerField(default=0)
    ascension_bonus_total = models.PositiveIntegerField(default=0)  # Cumulative +5 bonuses
    seasons_completed = models.PositiveIntegerField(default=0)
    
    highest_season_score = models.PositiveIntegerField(default=0)
    last_season_score = models.PositiveIntegerField(default=0)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.student.username} - Legacy: {self.total_legacy_points}"

    def add_season_score(self, season_score_obj):
        """Add season score and check for Ascension Bonus"""
        current_score = season_score_obj.total_score
        
        # Check for Ascension Bonus (current > previous)
        ascension_bonus = 0
        if self.last_season_score > 0 and current_score > self.last_season_score:
            ascension_bonus = 5
            self.ascension_bonus_total += ascension_bonus
        
        # Update totals
        self.total_legacy_points += current_score + ascension_bonus
        self.seasons_completed += 1
        
        # Update tracking
        if current_score > self.highest_season_score:
            self.highest_season_score = current_score
        self.last_season_score = current_score
        
        self.save()
        return ascension_bonus


class VaultWallet(models.Model):
    """
    Redeemable currency earned ONLY after full Season completion
    Spending does NOT reduce Legacy Score
    """
    student = models.OneToOneField(User, on_delete=models.CASCADE, related_name='vault_wallet')
    available_credits = models.PositiveIntegerField(default=0)
    total_earned = models.PositiveIntegerField(default=0)
    total_spent = models.PositiveIntegerField(default=0)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.student.username} - Credits: {self.available_credits}"

    def add_credits(self, amount, reason=""):
        """Add vault credits"""
        self.available_credits += amount
        self.total_earned += amount
        self.save()
        
        # Log transaction
        VaultTransaction.objects.create(
            wallet=self,
            transaction_type='earn',
            amount=amount,
            reason=reason
        )

    def spend_credits(self, amount, reason=""):
        """Spend vault credits"""
        if self.available_credits >= amount:
            self.available_credits -= amount
            self.total_spent += amount
            self.save()
            
            # Log transaction
            VaultTransaction.objects.create(
                wallet=self,
                transaction_type='spend',
                amount=amount,
                reason=reason
            )
            return True
        return False


class VaultTransaction(models.Model):
    """Track all vault credit transactions"""
    TRANSACTION_TYPES = [
        ('earn', 'Earned'),
        ('spend', 'Spent'),
    ]
    
    wallet = models.ForeignKey(VaultWallet, on_delete=models.CASCADE, related_name='transactions')
    transaction_type = models.CharField(max_length=10, choices=TRANSACTION_TYPES)
    amount = models.PositiveIntegerField()
    reason = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.wallet.student.username} - {self.transaction_type} {self.amount}"


class SCDStreak(models.Model):
    """
    Daily LeetCode streak verification
    Daily cron job syncs from LeetCode GraphQL API
    """
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='scd_streaks')
    season = models.ForeignKey(Season, on_delete=models.CASCADE, related_name='scd_streaks')
    
    leetcode_username = models.CharField(max_length=100)
    
    # Streak tracking
    current_streak = models.PositiveIntegerField(default=0)
    longest_streak = models.PositiveIntegerField(default=0)
    total_days_active = models.PositiveIntegerField(default=0)
    
    # Season-specific
    season_streak_days = models.PositiveIntegerField(default=0)
    streak_broken_count = models.PositiveIntegerField(default=0)
    last_synced_at = models.DateTimeField(null=True, blank=True)
    
    # Scoring
    streak_score = models.PositiveIntegerField(default=0, validators=[MaxValueValidator(100)])
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ['student', 'season']

    def __str__(self):
        return f"{self.student.username} - {self.season.name} - Streak: {self.current_streak}"

    def calculate_streak_score(self):
        """
        Calculate SCD score based on streak consistency
        Full uninterrupted streak = 100 points
        Partial breaks = reduced points
        """
        season_days = (self.season.end_date - self.season.start_date).days + 1
        
        if self.season_streak_days >= season_days - 2:  # Allow 2 day buffer
            self.streak_score = 100
        elif self.season_streak_days >= season_days * 0.8:
            self.streak_score = 80
        elif self.season_streak_days >= season_days * 0.6:
            self.streak_score = 60
        elif self.season_streak_days >= season_days * 0.4:
            self.streak_score = 40
        elif self.season_streak_days >= season_days * 0.2:
            self.streak_score = 20
        else:
            self.streak_score = 0
        
        self.save()
        return self.streak_score


class LeaderboardEntry(models.Model):
    """
    Champions Podium - Only Top 3 students per Season
    """
    season = models.ForeignKey(Season, on_delete=models.CASCADE, related_name='leaderboard')
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='leaderboard_entries')
    rank = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(3)])
    season_score = models.PositiveIntegerField()
    
    # Title
    RANK_TITLES = [
        (1, 'Season Champion'),
        (2, 'Elite Runner'),
        (3, 'Elite Runner'),
    ]
    rank_title = models.CharField(max_length=50)
    
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['season', 'rank']
        ordering = ['season', 'rank']

    def __str__(self):
        return f"{self.season.name} - Rank {self.rank}: {self.student.username}"


class Title(models.Model):
    """
    Redeemable titles using Vault Credits
    """
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField()
    vault_credit_cost = models.PositiveIntegerField()
    icon = models.CharField(max_length=50, blank=True)  # emoji or icon class
    rarity = models.CharField(max_length=20, choices=[
        ('common', 'Common'),
        ('rare', 'Rare'),
        ('epic', 'Epic'),
        ('legendary', 'Legendary'),
    ])
    is_active = models.BooleanField(default=True)
    
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.vault_credit_cost} credits)"


class UserTitle(models.Model):
    """
    Titles unlocked/equipped by students
    """
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='titles')
    title = models.ForeignKey(Title, on_delete=models.CASCADE, related_name='user_titles')
    is_equipped = models.BooleanField(default=False)
    unlocked_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['student', 'title']

    def __str__(self):
        return f"{self.student.username} - {self.title.name}"

    def equip(self):
        """Equip this title (unequip others)"""
        UserTitle.objects.filter(student=self.student, is_equipped=True).update(is_equipped=False)
        self.is_equipped = True
        self.save()


class PercentileBracket(models.Model):
    """
    Store percentile brackets for students not in top 3
    """
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='percentile_brackets')
    season = models.ForeignKey(Season, on_delete=models.CASCADE, related_name='percentile_brackets')
    percentile = models.CharField(max_length=20, choices=[
        ('top_10', 'Top 10%'),
        ('top_25', 'Top 25%'),
        ('top_50', 'Top 50%'),
        ('below_50', 'Below 50%'),
    ])
    season_score = models.PositiveIntegerField()
    
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['student', 'season']

    def __str__(self):
        return f"{self.student.username} - {self.season.name} - {self.percentile}"
