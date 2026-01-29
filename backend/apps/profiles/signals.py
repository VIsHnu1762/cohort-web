from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import FloorAnnouncement, UserProfile
from apps.dashboard.models import Notification


@receiver(post_save, sender=FloorAnnouncement)
def create_announcement_notifications(sender, instance, created, **kwargs):
    """
    Create notifications for all students and mentors on the floor
    when a new announcement is published
    """
    if created and instance.status == 'published':
        # Get all students on this floor
        students = UserProfile.objects.filter(
            campus=instance.campus,
            floor=instance.floor,
            role='STUDENT'
        ).select_related('user')
        
        # Get all mentors on this floor
        mentors = UserProfile.objects.filter(
            campus=instance.campus,
            floor=instance.floor,
            role='MENTOR'
        ).select_related('user')
        
        # Combine students and mentors
        recipients = list(students) + list(mentors)
        
        # Create notifications in bulk
        notifications = []
        priority_emoji = {
            'urgent': '🔴',
            'important': '🟠',
            'normal': '🔵'
        }
        
        emoji = priority_emoji.get(instance.priority, '🔵')
        
        for profile in recipients:
            notifications.append(
                Notification(
                    recipient=profile.user,
                    notification_type='announcement',
                    priority=instance.priority,
                    title=f"{emoji} {instance.title}",
                    message=instance.message[:200] + ('...' if len(instance.message) > 200 else ''),
                    related_submission_id=instance.id
                )
            )
        
        # Bulk create for performance
        if notifications:
            Notification.objects.bulk_create(notifications)
            print(f"✅ Created {len(notifications)} notifications for announcement: {instance.title}")
