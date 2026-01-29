"""
Progress Notification Service
Calculates batch averages and generates motivational notifications
"""
from django.contrib.auth import get_user_model
from django.db.models import Avg, Count, Q
from .models import EpisodeProgress, Season
import random

User = get_user_model()


class ProgressNotificationService:
    """
    Service to analyze student progress and generate motivational notifications
    """
    
    MOTIVATIONAL_MESSAGES = {
        'ahead': [
            "🔥 You're crushing it! Stay ahead of the pack!",
            "⭐ Outstanding performance! You're in the top tier!",
            "🚀 You're leading the charge! Keep up the momentum!",
            "💪 Exceptional progress! You're setting the bar high!",
            "🎯 You're ahead of the curve! Maintain this pace!",
        ],
        'on_track': [
            "👍 Great job! You're right on track with your batch!",
            "✨ Solid progress! Keep maintaining this steady pace!",
            "🎯 You're doing well! Stay consistent!",
            "💫 Good work! You're moving at the right pace!",
            "🌟 Nice progress! Keep it up!",
        ],
        'slightly_behind': [
            "⚡ You can catch up! Push a bit harder!",
            "🏃 Time to pick up the pace! You got this!",
            "💪 Your batch is moving ahead - let's go!",
            "🔥 Quick sprint needed! Close the gap!",
            "⏰ Time to accelerate! You're capable of more!",
        ],
        'behind': [
            "🚨 You're falling behind! Time to take action!",
            "⚠️ Your progress needs attention! Let's catch up!",
            "🏃‍♂️ Push yourself harder! The batch is moving ahead!",
            "💥 Wake-up call! It's time to hustle!",
            "🔴 Alert! You need to significantly speed up!",
        ],
        'far_behind': [
            "🚨 URGENT! You're significantly behind your batch!",
            "⛔ Critical: Immediate action required!",
            "🆘 You need to catch up fast! Talk to your mentor!",
            "🔥 Emergency mode! Time to go full throttle!",
            "💢 Major gap detected! Seek help and push hard!",
        ]
    }
    
    @classmethod
    def get_batch_statistics(cls, season=None):
        """
        Calculate batch-wide statistics for current season
        Returns total students, average progress, and distribution
        """
        if not season:
            season = Season.objects.filter(is_active=True).first()
        
        if not season:
            return None
        
        # Get all students who have episode progress
        students_with_progress = User.objects.filter(
            episode_progress__episode__season=season
        ).distinct()
        
        total_students = students_with_progress.count()
        
        if total_students == 0:
            return {
                'total_students': 0,
                'average_progress': 0,
                'season_name': season.name if season else None,
            }
        
        # Calculate average progress across all students
        avg_data = EpisodeProgress.objects.filter(
            episode__season=season,
            status__in=['unlocked', 'in_progress', 'completed']
        ).aggregate(
            avg_completion=Avg('completion_percentage')
        )
        
        # Count students in different progress ranges
        high_performers = EpisodeProgress.objects.filter(
            episode__season=season,
            completion_percentage__gte=75
        ).values('student').distinct().count()
        
        moderate_performers = EpisodeProgress.objects.filter(
            episode__season=season,
            completion_percentage__gte=40,
            completion_percentage__lt=75
        ).values('student').distinct().count()
        
        low_performers = EpisodeProgress.objects.filter(
            episode__season=season,
            completion_percentage__lt=40
        ).values('student').distinct().count()
        
        return {
            'total_students': total_students,
            'average_progress': round(avg_data['avg_completion'] or 0, 1),
            'high_performers': high_performers,
            'moderate_performers': moderate_performers,
            'low_performers': low_performers,
            'season_name': season.name,
            'season_id': season.id,
        }
    
    @classmethod
    def get_student_comparison(cls, student, season=None):
        """
        Compare individual student progress against batch average
        Returns comparison data and motivational message
        """
        if not season:
            season = Season.objects.filter(is_active=True).first()
        
        if not season:
            return None
        
        # Get batch statistics
        batch_stats = cls.get_batch_statistics(season)
        
        if not batch_stats or batch_stats['total_students'] == 0:
            return None
        
        # Get student's current episode progress
        try:
            current_progress = EpisodeProgress.objects.filter(
                student=student,
                episode__season=season,
                status__in=['unlocked', 'in_progress', 'completed']
            ).latest('episode__episode_number')
            
            student_progress = current_progress.completion_percentage
        except EpisodeProgress.DoesNotExist:
            student_progress = 0
        
        batch_average = batch_stats['average_progress']
        difference = student_progress - batch_average
        
        # Determine performance category
        if difference >= 20:
            category = 'ahead'
        elif difference >= 10:
            category = 'on_track'
        elif difference >= 0:
            category = 'on_track'
        elif difference >= -15:
            category = 'slightly_behind'
        elif difference >= -30:
            category = 'behind'
        else:
            category = 'far_behind'
        
        # Get random motivational message
        message = random.choice(cls.MOTIVATIONAL_MESSAGES[category])
        
        # Calculate percentile rank
        students_below = EpisodeProgress.objects.filter(
            episode__season=season,
            completion_percentage__lt=student_progress
        ).values('student').distinct().count()
        
        percentile = 0
        if batch_stats['total_students'] > 0:
            percentile = round((students_below / batch_stats['total_students']) * 100, 1)
        
        return {
            'student_progress': round(student_progress, 1),
            'batch_average': batch_average,
            'difference': round(difference, 1),
            'category': category,
            'message': message,
            'percentile_rank': percentile,
            'total_students': batch_stats['total_students'],
            'should_show_alert': category in ['slightly_behind', 'behind', 'far_behind'],
            'urgency_level': cls._get_urgency_level(category),
        }
    
    @classmethod
    def _get_urgency_level(cls, category):
        """
        Return urgency level for frontend styling
        """
        urgency_map = {
            'ahead': 'success',
            'on_track': 'info',
            'slightly_behind': 'warning',
            'behind': 'danger',
            'far_behind': 'critical',
        }
        return urgency_map.get(category, 'info')
