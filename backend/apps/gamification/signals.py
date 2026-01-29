from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from .models import LegacyScore, VaultWallet, Season, Episode, EpisodeProgress

User = get_user_model()


@receiver(post_save, sender=User)
def create_gamification_records(sender, instance, created, **kwargs):
    """Create LegacyScore and VaultWallet for new users"""
    if created:
        LegacyScore.objects.get_or_create(student=instance)
        VaultWallet.objects.get_or_create(student=instance)


@receiver(post_save, sender=Season)
def create_episodes_for_season(sender, instance, created, **kwargs):
    """Auto-create 4 episodes when a new season is created"""
    if created:
        from datetime import timedelta
        
        # Calculate episode dates (7 days each)
        episode_configs = [
            (1, 'Episode 1 - Kickoff'),
            (2, 'Episode 2 - Build'),
            (3, 'Episode 3 - Intensity'),
            (4, 'Episode 4 - Finale'),
        ]
        
        for i, (num, name) in enumerate(episode_configs):
            start = instance.start_date + timedelta(days=i * 7)
            end = start + timedelta(days=6)
            
            Episode.objects.create(
                season=instance,
                episode_number=num,
                name=name,
                start_date=start,
                end_date=end
            )


@receiver(post_save, sender=Episode)
def initialize_student_episode_progress(sender, instance, created, **kwargs):
    """Create EpisodeProgress for all students when new episode is created"""
    if created and instance.episode_number == 1:
        # Only Episode 1 starts unlocked
        students = User.objects.filter(profile__role='STUDENT')
        for student in students:
            EpisodeProgress.objects.create(
                student=student,
                episode=instance,
                status='unlocked'
            )
    elif created:
        # Episodes 2-4 start locked
        students = User.objects.filter(profile__role='STUDENT')
        for student in students:
            EpisodeProgress.objects.create(
                student=student,
                episode=instance,
                status='locked'
            )
