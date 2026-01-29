from django.contrib import admin
from .models import (
    HackathonSubmission,
    BMCVideoSubmission,
    InternshipSubmission,
    GenAIProjectSubmission
)


@admin.register(HackathonSubmission)
class HackathonSubmissionAdmin(admin.ModelAdmin):
    list_display = ['hackathon_name', 'user', 'mode', 'participation_date', 'status', 'created_at']
    list_filter = ['status', 'mode', 'created_at']
    search_fields = ['hackathon_name', 'user__username', 'user__email']
    readonly_fields = ['created_at', 'updated_at', 'submitted_at']
    
    fieldsets = (
        ('Hackathon Information', {
            'fields': ('user', 'hackathon_name', 'mode', 'registration_date', 'participation_date')
        }),
        ('Certificate', {
            'fields': ('certificate_link',)
        }),
        ('Submission Status', {
            'fields': ('status', 'current_step', 'submitted_at')
        }),
        ('Review', {
            'fields': ('reviewer_comments', 'reviewed_by', 'reviewed_at')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(BMCVideoSubmission)
class BMCVideoSubmissionAdmin(admin.ModelAdmin):
    list_display = ['user', 'video_url', 'status', 'created_at']
    list_filter = ['status', 'created_at']
    search_fields = ['user__username', 'user__email', 'description']
    readonly_fields = ['created_at', 'updated_at', 'submitted_at']
    
    fieldsets = (
        ('Video Information', {
            'fields': ('user', 'video_url', 'description')
        }),
        ('Submission Status', {
            'fields': ('status', 'submitted_at')
        }),
        ('Review', {
            'fields': ('reviewer_comments', 'reviewed_by', 'reviewed_at')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(InternshipSubmission)
class InternshipSubmissionAdmin(admin.ModelAdmin):
    list_display = ['user', 'role', 'company', 'internship_status', 'mode', 'status', 'created_at']
    list_filter = ['status', 'internship_status', 'mode', 'created_at']
    search_fields = ['company', 'role', 'user__username', 'user__email']
    readonly_fields = ['created_at', 'updated_at', 'submitted_at']
    
    fieldsets = (
        ('Internship Information', {
            'fields': ('user', 'company', 'role', 'mode', 'duration', 'internship_status')
        }),
        ('Documents', {
            'fields': ('completion_certificate_link', 'lor_link')
        }),
        ('Submission Status', {
            'fields': ('status', 'submitted_at')
        }),
        ('Review', {
            'fields': ('reviewer_comments', 'reviewed_by', 'reviewed_at')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(GenAIProjectSubmission)
class GenAIProjectSubmissionAdmin(admin.ModelAdmin):
    list_display = ['user', 'solution_type', 'innovation_industry', 'status', 'created_at']
    list_filter = ['status', 'solution_type', 'innovation_industry', 'created_at']
    search_fields = ['problem_statement', 'user__username', 'user__email', 'github_repo']
    readonly_fields = ['created_at', 'updated_at', 'submitted_at']
    
    fieldsets = (
        ('Project Information', {
            'fields': ('user', 'problem_statement', 'solution_type', 'innovation_technology', 'innovation_industry')
        }),
        ('Links', {
            'fields': ('github_repo', 'demo_link')
        }),
        ('Submission Status', {
            'fields': ('status', 'current_step', 'submitted_at')
        }),
        ('Review', {
            'fields': ('reviewer_comments', 'reviewed_by', 'reviewed_at')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
