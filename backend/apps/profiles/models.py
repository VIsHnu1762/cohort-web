from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone


class UserProfile(models.Model):
    """Extended user profile with platform IDs"""
    
    ROLE_CHOICES = [
        ('STUDENT', 'Student'),
        ('MENTOR', 'Mentor'),
        ('FLOOR_WING', 'Floor Wing'),
        ('ADMIN', 'Admin'),
    ]
    
    CAMPUS_CHOICES = [
        ('TECH', 'Dr. SNS Rajalakshmi College of Arts and Science'),
        ('ARTS', 'SNS College of Technology'),
    ]
    
    FLOOR_CHOICES = [
        (1, '1st Year'),
        (2, '2nd Year'),
        (3, '3rd Year'),
        (4, '4th Year'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    
    # Role and Campus/Floor assignment
    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default='STUDENT',
        help_text="User role in the system"
    )
    campus = models.CharField(
        max_length=10,
        choices=CAMPUS_CHOICES,
        null=True,
        blank=True,
        help_text="Campus assignment (Tech or Arts)"
    )
    floor = models.IntegerField(
        choices=FLOOR_CHOICES,
        null=True,
        blank=True,
        help_text="Floor/Year assignment (1-4 for Tech, 1-3 for Arts)"
    )
    
    # Mentor assignment (for students only)
    assigned_mentor = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='mentored_students',
        help_text="Mentor assigned to this student"
    )
    
    # Platform IDs
    leetcode_id = models.CharField(max_length=100, blank=True, null=True, help_text="LeetCode username")
    github_id = models.CharField(max_length=100, blank=True, null=True, help_text="GitHub username")
    linkedin_id = models.CharField(max_length=100, blank=True, null=True, help_text="LinkedIn profile URL or ID")
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "User Profile"
        verbose_name_plural = "User Profiles"
        indexes = [
            models.Index(fields=['user']),
            models.Index(fields=['role']),
            models.Index(fields=['campus', 'floor']),
            models.Index(fields=['assigned_mentor']),
        ]
    
    def __str__(self):
        campus_str = f" - {self.get_campus_display()}" if self.campus else ""
        floor_str = f" - Floor {self.floor}" if self.floor else ""
        return f"{self.user.username} ({self.get_role_display()}){campus_str}{floor_str}"
    
    def clean(self):
        """Validate campus and floor combinations"""
        from django.core.exceptions import ValidationError
        
        if self.campus == 'TECH' and self.floor and self.floor not in [1, 2, 3, 4]:
            raise ValidationError("Tech campus only has floors 1-4")
        if self.campus == 'ARTS' and self.floor and self.floor not in [1, 2, 3]:
            raise ValidationError("Arts campus only has floors 1-3")
        
        # Floor Wing and Mentors must have campus and floor
        if self.role in ['FLOOR_WING', 'MENTOR'] and (not self.campus or not self.floor):
            raise ValidationError(f"{self.get_role_display()} must be assigned to a campus and floor")
        
        # Students should have campus and floor
        if self.role == 'STUDENT' and (not self.campus or not self.floor):
            raise ValidationError("Students must be assigned to a campus and floor")


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """Automatically create profile when user is created (except during admin inline saves)"""
    if created:
        # Check if this is being called from within a bulk operation or has profile already
        if not hasattr(instance, '_profile_creation_skip'):
            UserProfile.objects.get_or_create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    """Save profile when user is saved"""
    # Ensure profile exists (for existing users without profiles)
    if not hasattr(instance, 'profile'):
        UserProfile.objects.get_or_create(user=instance)


# Floor Announcements Model
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
