from django.db import models
from django.contrib.auth.models import User
from django.core.validators import URLValidator
from django.utils import timezone


class HackathonRegistration(models.Model):
    """Track hackathons that students plan to participate in"""
    
    MODE_CHOICES = [
        ('online', 'Online'),
        ('offline', 'Offline'),
        ('hybrid', 'Hybrid'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='registered_hackathons')
    hackathon_name = models.CharField(max_length=255, help_text="Name of the hackathon")
    mode = models.CharField(max_length=20, choices=MODE_CHOICES, help_text="Participation mode")
    registration_date = models.DateField(help_text="Date when you registered")
    participation_date = models.DateField(help_text="Scheduled participation date")
    hackathon_url = models.URLField(max_length=500, blank=True, null=True, 
                                    help_text="Hackathon website or registration link")
    notes = models.TextField(blank=True, null=True, help_text="Personal notes or preparation goals")
    
    # Tracking
    is_completed = models.BooleanField(default=False, help_text="Mark as completed after participation")
    reminder_sent = models.BooleanField(default=False, help_text="Track if reminder was shown")
    
    # Link to submission (if created later)
    submission = models.OneToOneField('HackathonSubmission', on_delete=models.SET_NULL, 
                                     null=True, blank=True, related_name='registration')
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-participation_date', '-created_at']
        indexes = [
            models.Index(fields=['user', 'is_completed']),
            models.Index(fields=['participation_date']),
        ]
    
    def __str__(self):
        return f"{self.user.username} - {self.hackathon_name} (Registered)"
    
    @property
    def days_until_event(self):
        """Calculate days remaining until participation date"""
        from datetime import date
        delta = self.participation_date - date.today()
        return delta.days
    
    @property
    def is_upcoming(self):
        """Check if hackathon is upcoming (not completed and date is in future)"""
        from datetime import date
        return not self.is_completed and self.participation_date >= date.today()


class HackathonSubmission(models.Model):
    """Hackathon participation and achievement tracking"""
    
    MODE_CHOICES = [
        ('online', 'Online'),
        ('offline', 'Offline'),
        ('hybrid', 'Hybrid'),
    ]
    
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('submitted', 'Submitted'),
        ('under_review', 'Under Review'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='hackathons')
    hackathon_name = models.CharField(max_length=255, help_text="Name of the hackathon")
    mode = models.CharField(max_length=20, choices=MODE_CHOICES, help_text="Participation mode")
    registration_date = models.DateField(help_text="Date of registration")
    participation_date = models.DateField(help_text="Date of participation")
    github_repo = models.URLField(max_length=500, blank=True, null=True, 
                                  help_text="GitHub repository link for hackathon project")
    certificate_link = models.URLField(max_length=500, blank=True, null=True, 
                                       help_text="Google Drive link to certificate")
    
    # Status and review
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    current_step = models.IntegerField(default=1, help_text="Current step in submission process")
    submitted_at = models.DateTimeField(null=True, blank=True)
    
    # Review fields
    reviewer_comments = models.TextField(blank=True, null=True)
    reviewed_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, 
                                    related_name='reviewed_hackathons')
    reviewed_at = models.DateTimeField(null=True, blank=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user', 'status']),
            models.Index(fields=['created_at']),
        ]
    
    def __str__(self):
        return f"{self.user.username} - {self.hackathon_name}"


class BMCVideoSubmission(models.Model):
    """Business Model Canvas video submission"""
    
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('submitted', 'Submitted'),
        ('under_review', 'Under Review'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bmc_videos')
    video_url = models.URLField(max_length=500, help_text="YouTube or Drive link to BMC video")
    description = models.TextField(blank=True, null=True, help_text="Optional description of the BMC")
    
    # Status and review
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    submitted_at = models.DateTimeField(null=True, blank=True)
    
    # Review fields
    reviewer_comments = models.TextField(blank=True, null=True)
    reviewed_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, 
                                    related_name='reviewed_bmc_videos')
    reviewed_at = models.DateTimeField(null=True, blank=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user', 'status']),
        ]
    
    def __str__(self):
        return f"{self.user.username} - BMC Video"


class InternshipSubmission(models.Model):
    """Internship tracking with multi-step progress"""
    
    MODE_CHOICES = [
        ('remote', 'Remote'),
        ('onsite', 'On-site'),
        ('hybrid', 'Hybrid'),
    ]
    
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('submitted', 'Submitted'),
        ('under_review', 'Under Review'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]
    
    INTERNSHIP_STATUS_CHOICES = [
        (1, 'Application'),
        (2, 'Interview'),
        (3, 'Offer'),
        (4, 'Completion'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='internships')
    company = models.CharField(max_length=255, help_text="Company name")
    role = models.CharField(max_length=255, help_text="Internship role/position")
    mode = models.CharField(max_length=20, choices=MODE_CHOICES, help_text="Work mode")
    duration = models.CharField(max_length=100, help_text="Duration (e.g., '3 months', 'Summer 2025')")
    
    # Internship progress tracking
    internship_status = models.IntegerField(choices=INTERNSHIP_STATUS_CHOICES, default=1,
                                           help_text="Current stage of internship")
    
    # Document links
    completion_certificate_link = models.URLField(max_length=500, blank=True, null=True,
                                                  help_text="Google Drive link to completion certificate")
    lor_link = models.URLField(max_length=500, blank=True, null=True,
                               help_text="Google Drive link to Letter of Recommendation")
    
    # Status and review
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    submitted_at = models.DateTimeField(null=True, blank=True)
    
    # Review fields
    reviewer_comments = models.TextField(blank=True, null=True)
    reviewed_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, 
                                    related_name='reviewed_internships')
    reviewed_at = models.DateTimeField(null=True, blank=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user', 'status']),
            models.Index(fields=['company']),
        ]
    
    def __str__(self):
        return f"{self.user.username} - {self.role} at {self.company}"


class GenAIProjectSubmission(models.Model):
    """Generative AI Project submission"""
    
    SOLUTION_TYPE_CHOICES = [
        ('web_app', 'Web Application'),
        ('mobile_app', 'Mobile Application'),
        ('api', 'API/Backend Service'),
        ('ml_model', 'ML Model'),
        ('chatbot', 'Chatbot'),
        ('other', 'Other'),
    ]
    
    INDUSTRY_CHOICES = [
        ('healthcare', 'Healthcare'),
        ('finance', 'Finance'),
        ('education', 'Education'),
        ('ecommerce', 'E-commerce'),
        ('entertainment', 'Entertainment'),
        ('agriculture', 'Agriculture'),
        ('manufacturing', 'Manufacturing'),
        ('other', 'Other'),
    ]
    
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('submitted', 'Submitted'),
        ('under_review', 'Under Review'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='genai_projects')
    problem_statement = models.TextField(help_text="Description of the problem being solved")
    solution_type = models.CharField(max_length=200, blank=True, 
                                    help_text="Type of solution")
    innovation_technology = models.TextField(help_text="Technologies and innovations used")
    innovation_industry = models.CharField(max_length=200, blank=True,
                                          help_text="Target industry")
    github_repo = models.URLField(max_length=500, help_text="GitHub repository link")
    demo_link = models.URLField(max_length=500, blank=True, null=True, 
                                help_text="Optional demo/deployment link")
    
    # Status and review
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    current_step = models.IntegerField(default=1, help_text="Current step in submission process")
    submitted_at = models.DateTimeField(null=True, blank=True)
    
    # Review fields
    reviewer_comments = models.TextField(blank=True, null=True)
    reviewed_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, 
                                    related_name='reviewed_genai_projects')
    reviewed_at = models.DateTimeField(null=True, blank=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user', 'status']),
            models.Index(fields=['innovation_industry']),
        ]
    
    def __str__(self):
        return f"{self.user.username} - GenAI Project"
