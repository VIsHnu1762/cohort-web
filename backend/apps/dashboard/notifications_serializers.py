"""
Serializers for Notifications, Messages, and Announcements
"""

from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Notification, Message, MessageThread, Announcement


class UserBasicSerializer(serializers.ModelSerializer):
    """Basic user info for notifications and messages"""
    full_name = serializers.SerializerMethodField()
    avatar = serializers.SerializerMethodField()
    
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'full_name', 'avatar']
    
    def get_full_name(self, obj):
        return obj.get_full_name() or obj.username
    
    def get_avatar(self, obj):
        return obj.first_name[0].upper() if obj.first_name else obj.username[0].upper()


class NotificationSerializer(serializers.ModelSerializer):
    """Notification serializer"""
    sender = UserBasicSerializer(read_only=True)
    time_ago = serializers.SerializerMethodField()
    
    class Meta:
        model = Notification
        fields = [
            'id', 'sender', 'notification_type', 'priority', 'title', 'message',
            'related_pillar', 'related_submission_type', 'related_submission_id',
            'action_url', 'is_read', 'read_at', 'created_at', 'time_ago'
        ]
        read_only_fields = ['id', 'created_at', 'read_at']
    
    def get_time_ago(self, obj):
        """Calculate time ago string"""
        from django.utils import timezone
        delta = timezone.now() - obj.created_at
        
        if delta.seconds < 60:
            return "Just now"
        elif delta.seconds < 3600:
            minutes = delta.seconds // 60
            return f"{minutes}m ago"
        elif delta.seconds < 86400:
            hours = delta.seconds // 3600
            return f"{hours}h ago"
        elif delta.days < 7:
            return f"{delta.days}d ago"
        elif delta.days < 30:
            weeks = delta.days // 7
            return f"{weeks}w ago"
        else:
            return obj.created_at.strftime("%b %d, %Y")


class MessageSerializer(serializers.ModelSerializer):
    """Message serializer"""
    sender = UserBasicSerializer(read_only=True)
    recipient = UserBasicSerializer(read_only=True)
    time_ago = serializers.SerializerMethodField()
    
    class Meta:
        model = Message
        fields = [
            'id', 'sender', 'recipient', 'subject', 'message',
            'related_pillar', 'related_submission_type', 'related_submission_id',
            'status', 'is_read', 'read_at', 'parent_message',
            'created_at', 'updated_at', 'time_ago'
        ]
        read_only_fields = ['id', 'status', 'created_at', 'updated_at', 'read_at']
    
    def get_time_ago(self, obj):
        """Calculate time ago string"""
        from django.utils import timezone
        delta = timezone.now() - obj.created_at
        
        if delta.seconds < 60:
            return "Just now"
        elif delta.seconds < 3600:
            minutes = delta.seconds // 60
            return f"{minutes}m ago"
        elif delta.seconds < 86400:
            hours = delta.seconds // 3600
            return f"{hours}h ago"
        elif delta.days < 7:
            return f"{delta.days}d ago"
        elif delta.days < 30:
            weeks = delta.days // 7
            return f"{weeks}w ago"
        else:
            return obj.created_at.strftime("%b %d, %Y")


class MessageThreadSerializer(serializers.ModelSerializer):
    """Message thread serializer"""
    participant1 = UserBasicSerializer(read_only=True)
    participant2 = UserBasicSerializer(read_only=True)
    last_message = MessageSerializer(read_only=True)
    other_participant = serializers.SerializerMethodField()
    unread_count = serializers.SerializerMethodField()
    
    class Meta:
        model = MessageThread
        fields = [
            'id', 'participant1', 'participant2', 'other_participant',
            'last_message', 'last_message_at', 'unread_count',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'last_message_at']
    
    def get_other_participant(self, obj):
        """Get the other participant based on current user"""
        request = self.context.get('request')
        if request and request.user:
            other = obj.get_other_participant(request.user)
            return UserBasicSerializer(other).data
        return None
    
    def get_unread_count(self, obj):
        """Get unread count for current user"""
        request = self.context.get('request')
        if request and request.user:
            return obj.get_unread_count(request.user)
        return 0


class MessageCreateSerializer(serializers.Serializer):
    """Serializer for creating messages"""
    recipient_id = serializers.IntegerField()
    subject = serializers.CharField(max_length=255, required=False, allow_blank=True)
    message = serializers.CharField()
    related_pillar = serializers.CharField(max_length=20, required=False, allow_blank=True)
    related_submission_type = serializers.CharField(max_length=50, required=False, allow_blank=True)
    related_submission_id = serializers.IntegerField(required=False, allow_null=True)
    parent_message_id = serializers.IntegerField(required=False, allow_null=True)
    
    def validate_recipient_id(self, value):
        """Validate recipient exists"""
        try:
            User.objects.get(id=value)
        except User.DoesNotExist:
            raise serializers.ValidationError("Recipient not found")
        return value
    
    def validate_parent_message_id(self, value):
        """Validate parent message exists if provided"""
        if value:
            try:
                Message.objects.get(id=value)
            except Message.DoesNotExist:
                raise serializers.ValidationError("Parent message not found")
        return value


class AnnouncementSerializer(serializers.ModelSerializer):
    """Announcement serializer"""
    mentor = UserBasicSerializer(read_only=True)
    time_ago = serializers.SerializerMethodField()
    is_read = serializers.SerializerMethodField()
    
    class Meta:
        model = Announcement
        fields = [
            'id', 'mentor', 'title', 'description', 'category', 'priority',
            'event_date', 'created_at', 'updated_at', 'time_ago', 'is_read',
            'company_name', 'job_location', 'job_mode', 'job_duration', 
            'job_stipend', 'application_url', 'application_deadline', 'required_skills'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']
    
    def get_is_read(self, obj):
        """Check if current user has read this announcement"""
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            from apps.dashboard.models import AnnouncementRead
            return AnnouncementRead.objects.filter(announcement=obj, user=request.user).exists()
        return False
    
    def get_time_ago(self, obj):
        """Calculate time ago string"""
        from django.utils import timezone
        delta = timezone.now() - obj.created_at
        
        if delta.seconds < 60:
            return "Just now"
        elif delta.seconds < 3600:
            minutes = delta.seconds // 60
            return f"{minutes}m ago"
        elif delta.seconds < 86400:
            hours = delta.seconds // 3600
            return f"{hours}h ago"
        elif delta.days < 7:
            return f"{delta.days}d ago"
        elif delta.days < 30:
            weeks = delta.days // 7
            return f"{weeks}w ago"
        else:
            months = delta.days // 30
            return f"{months}mo ago"


class AnnouncementCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating announcements"""
    
    class Meta:
        model = Announcement
        fields = [
            'title', 'description', 'category', 'priority', 'event_date',
            'company_name', 'job_location', 'job_mode', 'job_duration',
            'job_stipend', 'application_url', 'application_deadline', 'required_skills'
        ]
    
    def validate_title(self, value):
        if len(value) < 3:
            raise serializers.ValidationError("Title must be at least 3 characters long")
        return value
    
    def validate_description(self, value):
        if len(value) < 5:
            raise serializers.ValidationError("Description must be at least 5 characters long")
        return value
    
    def validate(self, data):
        """Validate job/internship specific fields"""
        category = data.get('category')
        
        # If posting a job or internship, ensure required fields are present
        if category in ['job', 'internship']:
            required_job_fields = ['company_name', 'job_location', 'application_url']
            for field in required_job_fields:
                if not data.get(field):
                    raise serializers.ValidationError(
                        f"{field.replace('_', ' ').title()} is required for job/internship postings"
                    )
        
        return data
