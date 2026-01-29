from rest_framework import serializers
from .notification_models import Notification


class NotificationSerializer(serializers.ModelSerializer):
    """Serializer for user notifications"""
    time_ago = serializers.SerializerMethodField()
    
    class Meta:
        model = Notification
        fields = [
            'id', 'notification_type', 'title', 'message',
            'is_read', 'created_at', 'time_ago', 'announcement_id'
        ]
        read_only_fields = ['id', 'created_at', 'time_ago']
    
    def get_time_ago(self, obj):
        """Human-readable time ago"""
        from django.utils import timezone
        now = timezone.now()
        diff = now - obj.created_at
        
        seconds = diff.total_seconds()
        if seconds < 60:
            return 'Just now'
        elif seconds < 3600:
            mins = int(seconds / 60)
            return f'{mins} minute{"s" if mins != 1 else ""} ago'
        elif seconds < 86400:
            hours = int(seconds / 3600)
            return f'{hours} hour{"s" if hours != 1 else ""} ago'
        elif seconds < 604800:
            days = int(seconds / 86400)
            return f'{days} day{"s" if days != 1 else ""} ago'
        else:
            return obj.created_at.strftime('%b %d, %Y')
