from django.contrib import admin
from .models import LeetCodeProfile, LeetCodeSubmission, ProgressSnapshot


class LeetCodeSubmissionInline(admin.TabularInline):
    """Inline for recent submissions"""
    model = LeetCodeSubmission
    extra = 0
    fields = ['problem_title', 'difficulty', 'status', 'language', 'timestamp']
    readonly_fields = ['problem_title', 'difficulty', 'status', 'language', 'timestamp']
    can_delete = False
    max_num = 10


class ProgressSnapshotInline(admin.TabularInline):
    """Inline for progress snapshots"""
    model = ProgressSnapshot
    extra = 0
    fields = ['snapshot_date', 'total_solved', 'easy_solved', 'medium_solved', 'hard_solved', 'ranking']
    readonly_fields = ['snapshot_date', 'total_solved', 'easy_solved', 'medium_solved', 'hard_solved', 'ranking']
    can_delete = False
    max_num = 5


@admin.register(LeetCodeProfile)
class LeetCodeProfileAdmin(admin.ModelAdmin):
    """Admin interface for LeetCode profiles"""
    
    list_display = [
        'user', 'leetcode_username', 'total_solved', 'ranking',
        'status', 'submitted_at', 'reviewer'
    ]
    list_filter = ['status', 'created_at', 'submitted_at']
    search_fields = ['user__username', 'user__email', 'leetcode_username']
    readonly_fields = ['created_at', 'updated_at', 'last_synced', 'submitted_at', 'reviewed_at']
    
    fieldsets = (
        ('User Information', {
            'fields': ('user', 'leetcode_username')
        }),
        ('LeetCode Stats', {
            'fields': (
                'total_solved', 'easy_solved', 'medium_solved', 'hard_solved',
                'ranking', 'contest_rating', 'streak'
            )
        }),
        ('Submission', {
            'fields': ('screenshot_url', 'status', 'submitted_at')
        }),
        ('Review', {
            'fields': ('reviewer', 'reviewed_at', 'review_comments'),
            'classes': ('collapse',)
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at', 'last_synced'),
            'classes': ('collapse',)
        }),
    )
    
    inlines = [LeetCodeSubmissionInline, ProgressSnapshotInline]
    
    actions = ['approve_profiles', 'reject_profiles']
    
    def approve_profiles(self, request, queryset):
        """Bulk approve profiles"""
        from django.utils import timezone
        
        updated = queryset.filter(status='pending').update(
            status='approved',
            reviewer=request.user,
            reviewed_at=timezone.now()
        )
        
        self.message_user(request, f'{updated} profile(s) approved successfully.')
    
    approve_profiles.short_description = 'Approve selected profiles'
    
    def reject_profiles(self, request, queryset):
        """Bulk reject profiles"""
        from django.utils import timezone
        
        updated = queryset.filter(status='pending').update(
            status='rejected',
            reviewer=request.user,
            reviewed_at=timezone.now()
        )
        
        self.message_user(request, f'{updated} profile(s) rejected.')
    
    reject_profiles.short_description = 'Reject selected profiles'


@admin.register(LeetCodeSubmission)
class LeetCodeSubmissionAdmin(admin.ModelAdmin):
    """Admin interface for LeetCode submissions"""
    
    list_display = ['problem_title', 'difficulty', 'status', 'language', 'timestamp', 'profile']
    list_filter = ['difficulty', 'status', 'timestamp']
    search_fields = ['problem_title', 'problem_slug', 'profile__leetcode_username']
    readonly_fields = ['created_at']


@admin.register(ProgressSnapshot)
class ProgressSnapshotAdmin(admin.ModelAdmin):
    """Admin interface for progress snapshots"""
    
    list_display = ['profile', 'snapshot_date', 'total_solved', 'easy_solved', 'medium_solved', 'hard_solved', 'ranking']
    list_filter = ['snapshot_date']
    search_fields = ['profile__leetcode_username', 'profile__user__username']
    readonly_fields = ['snapshot_date']
