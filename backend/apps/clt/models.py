from django.db import models
from django.contrib.auth.models import User
from django.core.validators import FileExtensionValidator


class CLTSubmission(models.Model):
    """Creative Learning Track submission model"""
    
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('submitted', 'Submitted'),
        ('under_review', 'Under Review'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]
    
    # User and basic info
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='clt_submissions')
    
    # Course details (Step 1)
    title = models.CharField(max_length=255, help_text="Course title")
    description = models.TextField(help_text="Course description")
    platform = models.CharField(max_length=100, help_text="Learning platform (e.g., Coursera, Udemy)")
    completion_date = models.DateField(help_text="Date of course completion")
    duration = models.IntegerField(null=True, blank=True, help_text="Total course duration in hours")
    
    # Certificate/Evidence (Step 2)
    drive_link = models.URLField(max_length=500, blank=True, null=True, help_text="Google Drive link to certificate/evidence")
    
    # Submission metadata
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    current_step = models.IntegerField(default=1, help_text="Current step in submission process (1-3)")
    
    # Review and feedback
    reviewer_comments = models.TextField(blank=True, null=True)
    reviewed_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='clt_reviews')
    reviewed_at = models.DateTimeField(null=True, blank=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    submitted_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'CLT Submission'
        verbose_name_plural = 'CLT Submissions'
        indexes = [
            models.Index(fields=['user', '-created_at']),
            models.Index(fields=['user', 'status']),
            models.Index(fields=['status', '-created_at']),
            models.Index(fields=['submitted_at']),
        ]
    
    def __str__(self):
        return f"{self.user.username} - {self.title}"


class CLTFile(models.Model):
    """Files uploaded for CLT submission (certificates, evidence)"""
    
    FILE_TYPE_CHOICES = [
        ('certificate', 'Certificate'),
        ('evidence', 'Learning Evidence'),
        ('screenshot', 'Screenshot'),
        ('other', 'Other'),
    ]
    
    submission = models.ForeignKey(CLTSubmission, on_delete=models.CASCADE, related_name='files')
    file = models.FileField(
        upload_to='clt_submissions/%Y/%m/',
        validators=[FileExtensionValidator(allowed_extensions=['pdf', 'jpg', 'jpeg', 'png', 'doc', 'docx'])]
    )
    file_type = models.CharField(max_length=20, choices=FILE_TYPE_CHOICES, default='evidence')
    file_name = models.CharField(max_length=255)
    file_size = models.IntegerField(help_text="File size in bytes")
    uploaded_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['uploaded_at']
        verbose_name = 'CLT File'
        verbose_name_plural = 'CLT Files'
        indexes = [
            models.Index(fields=['submission', 'uploaded_at']),
        ]
    
    def __str__(self):
        return f"{self.submission.title} - {self.file_name}"
