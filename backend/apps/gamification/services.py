"""
Service layer for Gamification System
Handles scoring, episode progression, season finalization
"""
from django.db import transaction
from django.utils import timezone
from django.contrib.auth import get_user_model
from .models import (
    Season, Episode, EpisodeProgress, SeasonScore, LegacyScore,
    VaultWallet, SCDStreak, LeaderboardEntry, PercentileBracket
)

User = get_user_model()


class EpisodeService:
    """Handle episode progression and task completion"""
    
    @staticmethod
    def mark_task_completed(student, episode, task_type):
        """
        Mark a specific task as completed in an episode
        Called by mentor approval
        """
        progress, created = EpisodeProgress.objects.get_or_create(
            student=student,
            episode=episode
        )
        
        # Update task completion based on type
        task_field_map = {
            'clt': 'clt_completed',
            'cfc_task1': 'cfc_task1_completed',
            'cfc_task2': 'cfc_task2_completed',
            'cfc_task3': 'cfc_task3_completed',
            'iipc_task1': 'iipc_task1_completed',
            'iipc_task2': 'iipc_task2_completed',
            'sri': 'sri_completed',
            'scd_streak': 'scd_streak_active',
        }
        
        field_name = task_field_map.get(task_type)
        if field_name:
            setattr(progress, field_name, True)
            
            if progress.status == 'locked':
                progress.status = 'in_progress'
            if not progress.started_at:
                progress.started_at = timezone.now()
            
            progress.save()
            
            # Check if episode is now complete
            if progress.check_episode_completion():
                progress.mark_completed()
                return True, "Episode completed!"
        
        return False, "Task marked complete"
    
    @staticmethod
    def get_current_episode(student, season):
        """Get the current active episode for student"""
        # Find first non-completed episode
        progress = EpisodeProgress.objects.filter(
            student=student,
            episode__season=season,
            status__in=['unlocked', 'in_progress']
        ).order_by('episode__episode_number').first()
        
        return progress.episode if progress else None
    
    @staticmethod
    def unlock_episode(student, episode):
        """Manually unlock an episode"""
        progress, created = EpisodeProgress.objects.get_or_create(
            student=student,
            episode=episode,
            defaults={'status': 'unlocked'}
        )
        if not created and progress.status == 'locked':
            progress.status = 'unlocked'
            progress.save()


class SeasonScoringService:
    """Handle season score calculation and finalization"""
    
    @staticmethod
    @transaction.atomic
    def finalize_season(student, season):
        """
        Finalize season after all 4 episodes completed
        Calculate Season Score, update Legacy Score, allocate Vault Credits
        """
        # Check if all episodes are complete
        completed_episodes = EpisodeProgress.objects.filter(
            student=student,
            episode__season=season,
            status='completed'
        ).count()
        
        if completed_episodes != 4:
            return None, "Season not complete - all 4 episodes required"
        
        # Get or create season score
        season_score, created = SeasonScore.objects.get_or_create(
            student=student,
            season=season
        )
        
        if season_score.season_completed:
            return season_score, "Season already finalized"
        
        # Calculate pillar scores
        season_score.clt_score = SeasonScoringService._calculate_clt_score(student, season)
        season_score.iipc_score = SeasonScoringService._calculate_iipc_score(student, season)
        season_score.scd_score = SeasonScoringService._calculate_scd_score(student, season)
        season_score.cfc_score = SeasonScoringService._calculate_cfc_score(student, season)
        season_score.outcome_score = SeasonScoringService._calculate_outcome_score(student, season)
        
        season_score.calculate_total()
        season_score.season_completed = True
        season_score.completed_at = timezone.now()
        season_score.save()
        
        # Update Legacy Score with Ascension Bonus
        legacy_score, _ = LegacyScore.objects.get_or_create(student=student)
        ascension_bonus = legacy_score.add_season_score(season_score)
        
        # Allocate Vault Credits (1 credit per 10 points)
        vault_credits = season_score.total_score // 10
        wallet, _ = VaultWallet.objects.get_or_create(student=student)
        wallet.add_credits(vault_credits, f"Season {season.season_number} completion")
        
        # Update leaderboard
        SeasonScoringService._update_leaderboard(season)
        
        return season_score, f"Season finalized! Score: {season_score.total_score}, Ascension: +{ascension_bonus}, Credits: {vault_credits}"
    
    @staticmethod
    def _calculate_clt_score(student, season):
        """
        CLT: 100 points
        AI Certification (course completion + recommendation)
        """
        # Check for CLT submission in this season
        from apps.clt.models import CLTSubmission
        
        approved_submissions = CLTSubmission.objects.filter(
            user=student,
            status='approved',
            created_at__gte=season.start_date,
            created_at__lte=season.end_date
        ).count()
        
        if approved_submissions >= 1:
            return 100
        return 0
    
    @staticmethod
    def _calculate_iipc_score(student, season):
        """
        IIPC: 200 points
        - LinkedIn Connect (100 points)
        - LinkedIn Post/Article (100 points)
        """
        from apps.iipc.models import IIPCSubmission
        
        score = 0
        
        # Check for IIPC submissions
        submissions = IIPCSubmission.objects.filter(
            user=student,
            status='approved',
            created_at__gte=season.start_date,
            created_at__lte=season.end_date
        )
        
        # Simple scoring: 100 points per approved submission (max 2)
        score = min(submissions.count() * 100, 200)
        
        return score
    
    @staticmethod
    def _calculate_scd_score(student, season):
        """
        SCD: 100 points
        Daily LeetCode streak (full month = 100 points)
        """
        try:
            scd_streak = SCDStreak.objects.get(student=student, season=season)
            return scd_streak.calculate_streak_score()
        except SCDStreak.DoesNotExist:
            return 0
    
    @staticmethod
    def _calculate_cfc_score(student, season):
        """
        CFC: 800 points
        - BMC Video (200)
        - GenAI Project (200)
        - Hackathon Participation (200)
        - Patent/Journal (200)
        """
        from apps.cfc.models import CFCSubmission
        
        score = 0
        
        submissions = CFCSubmission.objects.filter(
            user=student,
            status='approved',
            created_at__gte=season.start_date,
            created_at__lte=season.end_date
        )
        
        # Award 200 points per submission, max 800
        score = min(submissions.count() * 200, 800)
        
        return score
    
    @staticmethod
    def _calculate_outcome_score(student, season):
        """
        Outcome: 300 points
        Internship or Placement >= 10 LPA
        """
        # This would need to be tracked separately
        # For now, return 0 unless manually set
        return 0
    
    @staticmethod
    def _update_leaderboard(season):
        """
        Update Champions Podium - Top 3 only
        Calculate percentile brackets for others
        """
        # Get all completed season scores
        completed_scores = SeasonScore.objects.filter(
            season=season,
            season_completed=True
        ).order_by('-total_score')
        
        # Clear existing leaderboard
        LeaderboardEntry.objects.filter(season=season).delete()
        PercentileBracket.objects.filter(season=season).delete()
        
        # Create top 3 leaderboard
        for idx, score in enumerate(completed_scores[:3], start=1):
            rank_title = 'Season Champion' if idx == 1 else 'Elite Runner'
            LeaderboardEntry.objects.create(
                season=season,
                student=score.student,
                rank=idx,
                season_score=score.total_score,
                rank_title=rank_title
            )
        
        # Calculate percentiles for others
        total_count = completed_scores.count()
        if total_count > 3:
            for score in completed_scores[3:]:
                # Calculate percentile
                rank_position = list(completed_scores.values_list('id', flat=True)).index(score.id) + 1
                percentile_value = (rank_position / total_count) * 100
                
                if percentile_value <= 10:
                    percentile = 'top_10'
                elif percentile_value <= 25:
                    percentile = 'top_25'
                elif percentile_value <= 50:
                    percentile = 'top_50'
                else:
                    percentile = 'below_50'
                
                PercentileBracket.objects.create(
                    student=score.student,
                    season=season,
                    percentile=percentile,
                    season_score=score.total_score
                )


class LeetCodeSyncService:
    """
    Service to sync LeetCode streak data
    Should be called by daily cron job
    """
    
    @staticmethod
    def sync_student_streak(student, season):
        """
        Sync LeetCode streak for a student
        Uses LeetCode GraphQL API
        """
        import requests
        
        # Get student's LeetCode username
        try:
            profile = student.profile
            leetcode_username = getattr(profile, 'leetcode_username', None)
            if not leetcode_username:
                return None, "No LeetCode username set"
        except:
            return None, "Profile not found"
        
        # Get or create streak record
        streak, created = SCDStreak.objects.get_or_create(
            student=student,
            season=season,
            defaults={'leetcode_username': leetcode_username}
        )
        
        # Call LeetCode GraphQL API
        url = "https://leetcode.com/graphql"
        query = """
        query userProfile($username: String!) {
            matchedUser(username: $username) {
                submitStats {
                    acSubmissionNum {
                        difficulty
                        count
                    }
                }
                profile {
                    ranking
                }
                userCalendar {
                    streak
                    totalActiveDays
                }
            }
        }
        """
        
        try:
            response = requests.post(
                url,
                json={
                    'query': query,
                    'variables': {'username': leetcode_username}
                },
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                user_data = data.get('data', {}).get('matchedUser', {})
                
                if user_data:
                    calendar_data = user_data.get('userCalendar', {})
                    current_streak = calendar_data.get('streak', 0)
                    total_active = calendar_data.get('totalActiveDays', 0)
                    
                    # Update streak record
                    streak.current_streak = current_streak
                    if current_streak > streak.longest_streak:
                        streak.longest_streak = current_streak
                    
                    streak.total_days_active = total_active
                    streak.season_streak_days += 1  # Increment season days
                    streak.last_synced_at = timezone.now()
                    streak.save()
                    
                    return streak, "Streak synced successfully"
            
            return None, f"API Error: {response.status_code}"
            
        except Exception as e:
            return None, f"Sync failed: {str(e)}"
    
    @staticmethod
    def sync_all_students(season):
        """Sync all students for a season - called by cron"""
        students = User.objects.filter(profile__role='STUDENT')
        results = {
            'success': 0,
            'failed': 0,
            'errors': []
        }
        
        for student in students:
            streak, message = LeetCodeSyncService.sync_student_streak(student, season)
            if streak:
                results['success'] += 1
            else:
                results['failed'] += 1
                results['errors'].append(f"{student.username}: {message}")
        
        return results


class TitleService:
    """Handle title redemption"""
    
    @staticmethod
    def redeem_title(student, title):
        """
        Redeem a title using Vault Credits
        """
        from .models import UserTitle
        
        # Check if already owned
        if UserTitle.objects.filter(student=student, title=title).exists():
            return False, "Title already owned"
        
        # Check wallet balance
        wallet, _ = VaultWallet.objects.get_or_create(student=student)
        if wallet.available_credits < title.vault_credit_cost:
            return False, "Insufficient Vault Credits"
        
        # Deduct credits
        if wallet.spend_credits(title.vault_credit_cost, f"Redeemed title: {title.name}"):
            # Create user title
            user_title = UserTitle.objects.create(
                student=student,
                title=title
            )
            return True, f"Title '{title.name}' redeemed successfully!"
        
        return False, "Transaction failed"
    
    @staticmethod
    def equip_title(student, title):
        """Equip a title"""
        try:
            user_title = UserTitle.objects.get(student=student, title=title)
            user_title.equip()
            return True, f"Title '{title.name}' equipped"
        except UserTitle.DoesNotExist:
            return False, "Title not owned"
