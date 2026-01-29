from django.contrib import admin
from .models import CLTSubmission, CLTFile


class CLTFileInline(admin.TabularInline):
    model = CLTFile
    extra = 0
    readonly_fields = ['file_name', 'file_size', 'uploaded_at']


@admin.register(CLTSubmission)
class CLTSubmissionAdmin(admin.ModelAdmin):
    list_display = ['title', 'user', 'platform', 'completion_date', 'duration', 'status', 'current_step', 'created_at']
    list_filter = ['status', 'platform', 'created_at']
    search_fields = ['title', 'description', 'user__username', 'user__email']
    readonly_fields = ['created_at', 'updated_at', 'submitted_at']
    inlines = [CLTFileInline]
    
    fieldsets = (
        ('Course Information', {
            'fields': ('user', 'title', 'description', 'platform', 'completion_date', 'duration')
        }),
        ('Certificate/Evidence', {
            'fields': ('drive_link',)
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


@admin.register(CLTFile)
class CLTFileAdmin(admin.ModelAdmin):
    list_display = ['file_name', 'submission', 'file_type', 'file_size', 'uploaded_at']
    list_filter = ['file_type', 'uploaded_at']
    search_fields = ['file_name', 'submission__title']
    readonly_fields = ['uploaded_at']
