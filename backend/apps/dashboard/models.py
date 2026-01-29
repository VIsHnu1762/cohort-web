from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Announcement(models.Model):
    """Announcements created by mentors for their students"""
    
    CATEGORY_CHOICES = [
        ('general', 'General'),
        ('event', 'Event'),
        ('deadline', 'Deadline'),
        ('important', 'Important'),
        ('reminder', 'Reminder'),
        ('job', 'Job Opportunity'),
        ('internship', 'Internship Opportunity'),
    ]
    
    PRIORITY_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
    ]
    
    JOB_MODE_CHOICES = [
        ('on-site', 'On-site'),
        ('remote', 'Remote'),
        ('hybrid', 'Hybrid'),
    ]
    
    mentor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='announcements_created')
    title = models.CharField(max_length=255)
    description = models.TextField()
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='general')
    priority = models.CharField(max_length=20, choices=PRIORITY_CHOICES, default='medium')
    
    # Optional deadline/event date
    event_date = models.DateField(null=True, blank=True, help_text="For deadlines or events")
    
    # Job/Internship specific fields
    company_name = models.CharField(max_length=255, null=True, blank=True, help_text="Company name for job/internship postings")
    job_location = models.CharField(max_length=255, null=True, blank=True, help_text="Job location")
    job_mode = models.CharField(max_length=20, choices=JOB_MODE_CHOICES, null=True, blank=True, help_text="Work mode")
    job_duration = models.CharField(max_length=100, null=True, blank=True, help_text="Duration (e.g., '6 months', 'Full-time')")
    job_stipend = models.CharField(max_length=100, null=True, blank=True, help_text="Stipend/Salary range")
    application_url = models.URLField(max_length=500, null=True, blank=True, help_text="Application link")
    application_deadline = models.DateField(null=True, blank=True, help_text="Last date to apply")
    required_skills = models.TextField(null=True, blank=True, help_text="Comma-separated skills")
    
    # Tracking
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['-created_at']),
            models.Index(fields=['mentor', '-created_at']),
        ]
    
    def __str__(self):
        return f"{self.title} by {self.mentor.username}"
    
    def save(self, *args, **kwargs):
        is_new = self.pk is None
        super().save(*args, **kwargs)
        
        # Create notifications for all students under this mentor when announcement is created
        if is_new:
            from apps.profiles.models import UserProfile
            students = UserProfile.objects.filter(assigned_mentor=self.mentor).select_related('user')
            notifications = []
            for student_profile in students:
                notifications.append(Notification(
                    recipient=student_profile.user,
                    sender=self.mentor,
                    notification_type='info',
                    priority=self.priority,
                    title=f"New Announcement: {self.title}",
                    message=self.description[:200] + ('...' if len(self.description) > 200 else ''),
                    action_url=f"/student/announcements"
                ))
            if notifications:
                Notification.objects.bulk_create(notifications)


class AnnouncementRead(models.Model):
    """Track which students have read which announcements"""
    announcement = models.ForeignKey(Announcement, on_delete=models.CASCADE, related_name='reads')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='announcement_reads')
    read_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('announcement', 'user')
        ordering = ['-read_at']
        indexes = [
            models.Index(fields=['user', '-read_at']),
            models.Index(fields=['announcement']),
        ]
    
    def __str__(self):
        return f"{self.user.username} read {self.announcement.title}"


class Notification(models.Model):
    """Enhanced notification model for mentor and student updates"""
    
    TYPE_CHOICES = [
        ('submission_approved', 'Submission Approved'),
        ('submission_rejected', 'Submission Rejected'),
        ('submission_resubmit', 'Resubmission Requested'),
        ('announcement', 'Announcement'),  # New type for announcements
        ('message', 'New Message'),
        ('info', 'Info'),
        ('warning', 'Warning'),
        ('success', 'Success'),
        ('error', 'Error'),
        ('general', 'General'),
    ]
    
    PRIORITY_CHOICES = [
        ('low', 'Low'),
        ('normal', 'Normal'),
        ('high', 'High'),
    ]
    
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    sender = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='sent_notifications')
    
    notification_type = models.CharField(max_length=50, choices=TYPE_CHOICES, default='general')
    priority = models.CharField(max_length=20, choices=PRIORITY_CHOICES, default='normal')
    
    title = models.CharField(max_length=255, default='Notification')
    message = models.TextField(help_text="Notification message")
    
    # Link to related object (optional)
    related_pillar = models.CharField(max_length=20, blank=True, null=True, help_text="cfc, clt, iipc, scd, sri")
    related_submission_type = models.CharField(max_length=50, blank=True, null=True)
    related_submission_id = models.IntegerField(blank=True, null=True)
    
    # URL to redirect user when they click on notification
    action_url = models.CharField(max_length=500, blank=True, null=True)
    
    # Status
    is_read = models.BooleanField(default=False)
    read_at = models.DateTimeField(null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['recipient', '-created_at']),
            models.Index(fields=['recipient', 'is_read']),
            models.Index(fields=['-created_at']),
        ]
    
    def __str__(self):
        return f"{self.recipient.username} - {self.title}"
    
    def mark_as_read(self):
        """Mark notification as read"""
        if not self.is_read:
            self.is_read = True
            self.read_at = timezone.now()
            self.save()


class Message(models.Model):
    """Direct messages between mentor and student"""
    
    STATUS_CHOICES = [
        ('sent', 'Sent'),
        ('delivered', 'Delivered'),
        ('read', 'Read'),
    ]
    
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_messages')
    
    subject = models.CharField(max_length=255, blank=True, null=True)
    message = models.TextField()
    
    # Link to related submission (optional)
    related_pillar = models.CharField(max_length=20, blank=True, null=True)
    related_submission_type = models.CharField(max_length=50, blank=True, null=True)
    related_submission_id = models.IntegerField(blank=True, null=True)
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='sent')
    is_read = models.BooleanField(default=False)
    read_at = models.DateTimeField(null=True, blank=True)
    
    # Parent message for threading
    parent_message = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='replies')
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['recipient', '-created_at']),
            models.Index(fields=['sender', '-created_at']),
            models.Index(fields=['recipient', 'is_read']),
            models.Index(fields=['-created_at']),
        ]
    
    def __str__(self):
        return f"{self.sender.username} → {self.recipient.username}: {self.subject or self.message[:50]}"
    
    def mark_as_read(self):
        """Mark message as read"""
        if not self.is_read:
            self.is_read = True
            self.read_at = timezone.now()
            self.status = 'read'
            self.save()


class MessageThread(models.Model):
    """Conversation thread between mentor and student"""
    
    participant1 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='threads_as_participant1')
    participant2 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='threads_as_participant2')
    
    last_message = models.ForeignKey(Message, on_delete=models.SET_NULL, null=True, blank=True, related_name='+')
    last_message_at = models.DateTimeField(auto_now_add=True)
    
    # Unread counts for each participant
    unread_count_p1 = models.IntegerField(default=0)
    unread_count_p2 = models.IntegerField(default=0)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-last_message_at']
        indexes = [
            models.Index(fields=['participant1', '-last_message_at']),
            models.Index(fields=['participant2', '-last_message_at']),
        ]
    
    def __str__(self):
        return f"Thread: {self.participant1.username} ↔ {self.participant2.username}"
    
    def get_other_participant(self, user):
        """Get the other participant in the thread"""
        if user == self.participant1:
            return self.participant2
        return self.participant1
    
    def get_unread_count(self, user):
        """Get unread count for a specific user"""
        if user == self.participant1:
            return self.unread_count_p1
        return self.unread_count_p2
    
    def increment_unread(self, user):
        """Increment unread count for a user"""
        if user == self.participant1:
            self.unread_count_p1 += 1
        else:
            self.unread_count_p2 += 1
        self.save()
    
    def reset_unread(self, user):
        """Reset unread count for a user"""
        if user == self.participant1:
            self.unread_count_p1 = 0
        else:
            self.unread_count_p2 = 0
        self.save()
