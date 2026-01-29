from django.contrib import admin
from .models import Notification, Message, MessageThread


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ['id', 'recipient', 'sender', 'notification_type', 'title', 'is_read', 'created_at']
    list_filter = ['notification_type', 'priority', 'is_read', 'created_at']
    search_fields = ['title', 'message', 'recipient__username', 'sender__username']
    readonly_fields = ['created_at', 'read_at']
    list_per_page = 50
    
    def message_preview(self, obj):
        return obj.message[:50] + '...' if len(obj.message) > 50 else obj.message
    message_preview.short_description = 'Message'


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ['id', 'sender', 'recipient', 'subject', 'message_preview', 'is_read', 'created_at']
    list_filter = ['status', 'is_read', 'created_at']
    search_fields = ['subject', 'message', 'sender__username', 'recipient__username']
    readonly_fields = ['created_at', 'updated_at', 'read_at']
    list_per_page = 50
    
    def message_preview(self, obj):
        return obj.message[:50] + '...' if len(obj.message) > 50 else obj.message
    message_preview.short_description = 'Message'


@admin.register(MessageThread)
class MessageThreadAdmin(admin.ModelAdmin):
    list_display = ['id', 'participant1', 'participant2', 'last_message_at', 'unread_count_p1', 'unread_count_p2']
    list_filter = ['created_at', 'last_message_at']
    search_fields = ['participant1__username', 'participant2__username']
    readonly_fields = ['created_at', 'updated_at']
    list_per_page = 50
