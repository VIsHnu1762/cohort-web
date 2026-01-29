from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class FloorAnnouncement(models.Model):
    """Floor-level announcements created by Floor Wing for their assigned floor"""
    
    PRIORITY_CHOICES = [
        ('normal', 'Normal'),
        ('important', 'Important'),
        ('urgent', 'Urgent'),
    ]
    
    CAMPUS_CHOICES = [
        ('TECH', 'Technology Campus'),
        ('ARTS', 'Arts & Science Campus'),
    ]
    
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('published', 'Published'),
        ('expired', 'Expired'),
    ]
    
    # Core fields
    floor_wing = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='floor_announcements_created'
    )
    title = models.CharField(max_length=255)
    message = models.TextField()
    priority = models.CharField(max_length=20, choices=PRIORITY_CHOICES, default='normal')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='published')
    
    # Scoping - CRITICAL for isolation
    campus = models.CharField(max_length=10, choices=CAMPUS_CHOICES)
    floor = models.IntegerField()
    
    # Optional expiry
    expires_at = models.DateTimeField(null=True, blank=True)
    
    # Tracking
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # Read tracking
    read_by = models.ManyToManyField(
        User, 
        related_name='read_floor_announcements', 
        blank=True
    )
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['campus', 'floor', 'status']),
            models.Index(fields=['created_at']),
        ]
        constraints = [
            models.CheckConstraint(
                check=models.Q(floor__gte=1) & models.Q(floor__lte=4),
                name='valid_floor_range'
            )
        ]
    
    def __str__(self):
        return f"{self.title} - {self.campus} Floor {self.floor}"
    
    @property
    def is_expired(self):
        """Check if announcement has expired"""
        if self.expires_at:
            return timezone.now() > self.expires_at
        return False
    
    @property
    def read_count(self):
        """Count of users who have read this announcement"""
        return self.read_by.count()
    
    def mark_as_read(self, user):
        """Mark announcement as read by a user"""
        if user not in self.read_by.all():
            self.read_by.add(user)
    
    def is_read_by(self, user):
        """Check if user has read this announcement"""
        return self.read_by.filter(id=user.id).exists()
