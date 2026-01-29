from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone

User = get_user_model()


class LeetCodeProfile(models.Model):
    """
    Stores LeetCode profile information for a student
    """
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('pending', 'Pending Review'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='leetcode_profiles')
    leetcode_username = models.CharField(max_length=100)
    
    # LeetCode Stats
    total_solved = models.IntegerField(default=0)
    easy_solved = models.IntegerField(default=0)
    medium_solved = models.IntegerField(default=0)
    hard_solved = models.IntegerField(default=0)
    
    ranking = models.IntegerField(null=True, blank=True)
    contest_rating = models.IntegerField(null=True, blank=True)
    streak = models.IntegerField(default=0)
    monthly_problems_count = models.IntegerField(default=0, help_text="Problems solved this month")
    total_active_days = models.IntegerField(default=0)
    submission_calendar = models.JSONField(default=dict, blank=True, help_text="Calendar data from LeetCode")
    
    # Submission tracking
    screenshot_url = models.URLField(max_length=500, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    
    # Metadata
    last_synced = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # Review tracking
    submitted_at = models.DateTimeField(null=True, blank=True)
    reviewed_at = models.DateTimeField(null=True, blank=True)
    reviewer = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='reviewed_leetcode_profiles'
    )
    review_comments = models.TextField(blank=True)
    
    class Meta:
        ordering = ['-created_at']
        unique_together = ['user', 'leetcode_username']
    
    def __str__(self):
        return f"{self.user.username} - {self.leetcode_username}"


class LeetCodeSubmission(models.Model):
    """
    Stores individual problem submissions from LeetCode
    """
    profile = models.ForeignKey(
        LeetCodeProfile, 
        on_delete=models.CASCADE, 
        related_name='submissions'
    )
    
    problem_title = models.CharField(max_length=200)
    problem_slug = models.CharField(max_length=200)
    difficulty = models.CharField(max_length=20)  # Easy, Medium, Hard
    status = models.CharField(max_length=50)  # Accepted, Wrong Answer, etc.
    language = models.CharField(max_length=50, blank=True)
    timestamp = models.DateTimeField()
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-timestamp']
    
    def __str__(self):
        return f"{self.problem_title} - {self.status}"


class ProgressSnapshot(models.Model):
    """
    Stores periodic snapshots of progress for tracking over time
    """
    profile = models.ForeignKey(
        LeetCodeProfile, 
        on_delete=models.CASCADE, 
        related_name='snapshots'
    )
    
    total_solved = models.IntegerField()
    easy_solved = models.IntegerField()
    medium_solved = models.IntegerField()
    hard_solved = models.IntegerField()
    ranking = models.IntegerField(null=True, blank=True)
    
    snapshot_date = models.DateTimeField(default=timezone.now)
    
    class Meta:
        ordering = ['-snapshot_date']
    
    def __str__(self):
        return f"{self.profile.leetcode_username} - {self.snapshot_date.date()}"
