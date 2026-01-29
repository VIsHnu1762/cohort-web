from django.contrib import admin
from .models import (
    LinkedInPostVerification,
    LinkedInConnectionVerification,
    ConnectionScreenshot,
    VerifiedConnection
)


class ConnectionScreenshotInline(admin.TabularInline):
    model = ConnectionScreenshot
    extra = 1
    fields = ['screenshot_url', 'uploaded_at']
    readonly_fields = ['uploaded_at']


class VerifiedConnectionInline(admin.TabularInline):
    model = VerifiedConnection
    extra = 1
    fields = ['name', 'company', 'designation', 'profile_url', 'is_verified']


@admin.register(LinkedInPostVerification)
class LinkedInPostVerificationAdmin(admin.ModelAdmin):
    list_display = ['user', 'post_date', 'character_count', 'hashtag_count', 'status', 'submitted_at']
    list_filter = ['status', 'post_date', 'submitted_at']
    search_fields = ['user__username', 'user__email', 'post_url']
    readonly_fields = ['created_at', 'updated_at', 'submitted_at']
    
    fieldsets = (
        ('User Information', {
            'fields': ('user', 'post_url', 'post_date')
        }),
        ('Post Metrics', {
            'fields': ('character_count', 'hashtag_count')
        }),
        ('Review', {
            'fields': ('status', 'reviewer_comments', 'reviewed_by', 'reviewed_at')
        }),
        ('Timestamps', {
            'fields': ('submitted_at', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def get_readonly_fields(self, request, obj=None):
        if obj and obj.status in ['approved', 'rejected']:
            return self.readonly_fields + ['status', 'reviewer_comments']
        return self.readonly_fields


@admin.register(LinkedInConnectionVerification)
class LinkedInConnectionVerificationAdmin(admin.ModelAdmin):
    list_display = ['user', 'verification_method', 'total_connections', 
                   'verified_connections_count', 'status', 'submitted_at']
    list_filter = ['status', 'verification_method', 'submitted_at']
    search_fields = ['user__username', 'user__email', 'profile_url']
    readonly_fields = ['created_at', 'updated_at', 'submitted_at', 'verified_connections_count']
    inlines = [ConnectionScreenshotInline, VerifiedConnectionInline]
    
    fieldsets = (
        ('User Information', {
            'fields': ('user', 'verification_method', 'profile_url')
        }),
        ('Connection Metrics', {
            'fields': ('total_connections', 'verified_connections_count')
        }),
        ('Review', {
            'fields': ('status', 'reviewer_comments', 'reviewed_by', 'reviewed_at')
        }),
        ('Timestamps', {
            'fields': ('submitted_at', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def get_readonly_fields(self, request, obj=None):
        if obj and obj.status in ['approved', 'rejected']:
            return self.readonly_fields + ['status', 'reviewer_comments']
        return self.readonly_fields


@admin.register(ConnectionScreenshot)
class ConnectionScreenshotAdmin(admin.ModelAdmin):
    list_display = ['verification', 'screenshot_url', 'uploaded_at']
    list_filter = ['uploaded_at']
    search_fields = ['verification__user__username']
    readonly_fields = ['uploaded_at']


@admin.register(VerifiedConnection)
class VerifiedConnectionAdmin(admin.ModelAdmin):
    list_display = ['name', 'company', 'designation', 'is_verified', 'verification']
    list_filter = ['is_verified', 'company']
    search_fields = ['name', 'company', 'designation', 'verification__user__username']
