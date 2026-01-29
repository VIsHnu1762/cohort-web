from django.db import models
from django.contrib.auth.models import User
from django.core.validators import URLValidator, MinValueValidator, MaxValueValidator


class LinkedInPostVerification(models.Model):
    """LinkedIn Post Verification Submission"""
    
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('pending', 'Pending Review'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='linkedin_posts')
    post_url = models.URLField(max_length=500, validators=[URLValidator()], 
                               help_text="LinkedIn post URL")
    
    # Post metrics (extracted or manually entered)
    post_date = models.DateField(help_text="Date when post was published")
    character_count = models.IntegerField(validators=[MinValueValidator(0)],
                                         help_text="Number of characters in post")
    hashtag_count = models.IntegerField(validators=[MinValueValidator(0)],
                                       help_text="Number of hashtags used")
    
    # Review fields
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    reviewer_comments = models.TextField(blank=True, null=True)
    reviewed_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True,
                                   related_name='reviewed_linkedin_posts')
    reviewed_at = models.DateTimeField(null=True, blank=True)
    
    # Timestamps
    submitted_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'LinkedIn Post Verification'
        verbose_name_plural = 'LinkedIn Post Verifications'
        indexes = [
            models.Index(fields=['user', 'status']),
            models.Index(fields=['post_date']),
        ]
    
    def __str__(self):
        return f"{self.user.username} - Post on {self.post_date}"


class LinkedInConnectionVerification(models.Model):
    """LinkedIn Connections Verification Submission"""
    
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('pending', 'Pending Review'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]
    
    VERIFICATION_METHOD_CHOICES = [
        ('screenshot', 'Screenshot Upload'),
        ('profile', 'Profile Link'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='linkedin_connections')
    verification_method = models.CharField(max_length=20, choices=VERIFICATION_METHOD_CHOICES,
                                          default='screenshot')
    
    # Profile link method
    profile_url = models.URLField(max_length=500, blank=True, null=True,
                                 validators=[URLValidator()],
                                 help_text="LinkedIn profile URL")
    
    # Connection metrics
    total_connections = models.IntegerField(validators=[MinValueValidator(0)],
                                           help_text="Total number of connections")
    verified_connections_count = models.IntegerField(default=0, 
                                                    validators=[MinValueValidator(0)],
                                                    help_text="Number of verified connections")
    
    # Review fields
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    reviewer_comments = models.TextField(blank=True, null=True)
    reviewed_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True,
                                   related_name='reviewed_linkedin_connections')
    reviewed_at = models.DateTimeField(null=True, blank=True)
    
    # Timestamps
    submitted_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'LinkedIn Connection Verification'
        verbose_name_plural = 'LinkedIn Connection Verifications'
        indexes = [
            models.Index(fields=['user', 'status']),
        ]
    
    def __str__(self):
        return f"{self.user.username} - {self.total_connections} connections"


class ConnectionScreenshot(models.Model):
    """Screenshots uploaded for LinkedIn connection verification"""
    
    verification = models.ForeignKey(LinkedInConnectionVerification, 
                                    on_delete=models.CASCADE, 
                                    related_name='screenshots')
    screenshot_url = models.URLField(max_length=500, help_text="Google Drive link to screenshot")
    uploaded_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['uploaded_at']
        verbose_name = 'Connection Screenshot'
        verbose_name_plural = 'Connection Screenshots'
    
    def __str__(self):
        return f"Screenshot for {self.verification.user.username}"


class VerifiedConnection(models.Model):
    """Individual verified LinkedIn connections"""
    
    verification = models.ForeignKey(LinkedInConnectionVerification,
                                    on_delete=models.CASCADE,
                                    related_name='verified_connections')
    name = models.CharField(max_length=200, help_text="Connection's name")
    company = models.CharField(max_length=200, blank=True, help_text="Current company")
    designation = models.CharField(max_length=200, blank=True, help_text="Job title")
    profile_url = models.URLField(max_length=500, blank=True, 
                                  help_text="LinkedIn profile URL")
    is_verified = models.BooleanField(default=False, 
                                     help_text="Whether connection is verified")
    
    class Meta:
        ordering = ['name']
        verbose_name = 'Verified Connection'
        verbose_name_plural = 'Verified Connections'
    
    def __str__(self):
        return f"{self.name} - {self.company}"
