from django.db import models
from django.contrib.auth.models import User


class Notification(models.Model):
    """User notifications for announcements and other events"""
    NOTIFICATION_TYPES = [
        ('floor_announcement', 'Floor Announcement'),
        ('mentor_message', 'Mentor Message'),
        ('submission_review', 'Submission Review'),
        ('system', 'System Notification'),
    ]
    
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='profile_notifications')
    notification_type = models.CharField(max_length=50, choices=NOTIFICATION_TYPES)
    title = models.CharField(max_length=255)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    # Optional: Link to related objects
    announcement_id = models.IntegerField(null=True, blank=True)
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['recipient', 'is_read']),
            models.Index(fields=['created_at']),
        ]
    
    def __str__(self):
        return f"{self.recipient.username} - {self.title}"
