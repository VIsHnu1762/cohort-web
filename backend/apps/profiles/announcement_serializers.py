from rest_framework import serializers
from django.contrib.auth.models import User
from .models import FloorAnnouncement


class FloorAnnouncementSerializer(serializers.ModelSerializer):
    """Serializer for Floor Announcements"""
    floor_wing_name = serializers.SerializerMethodField()
    is_expired = serializers.BooleanField(read_only=True)
    read_count = serializers.IntegerField(read_only=True)
    is_read = serializers.SerializerMethodField()
    expires_at = serializers.DateTimeField(required=False, allow_null=True)
    
    class Meta:
        model = FloorAnnouncement
        fields = [
            'id', 'title', 'message', 'priority', 'status',
            'campus', 'floor', 'expires_at',
            'floor_wing', 'floor_wing_name',
            'created_at', 'updated_at',
            'is_expired', 'read_count', 'is_read'
        ]
        read_only_fields = ['floor_wing', 'created_at', 'updated_at', 'campus', 'floor']
    
    def get_floor_wing_name(self, obj):
        """Get floor wing name"""
        return obj.floor_wing.get_full_name() or obj.floor_wing.username
    
    def get_is_read(self, obj):
        """Check if current user has read this announcement"""
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return obj.is_read_by(request.user)
        return False
    
    def validate_expires_at(self, value):
        """Convert empty string to None"""
        if value == '':
            return None
        return value
    
    def create(self, validated_data):
        """Auto-set floor wing, campus, and floor from request user"""
        request = self.context.get('request')
        user = request.user
        
        # Get floor wing's campus and floor
        validated_data['floor_wing'] = user
        validated_data['campus'] = user.profile.campus
        validated_data['floor'] = user.profile.floor
        
        return super().create(validated_data)


class FloorAnnouncementListSerializer(serializers.ModelSerializer):
    """Lightweight serializer for listing announcements"""
    floor_wing_name = serializers.SerializerMethodField()
    is_read = serializers.SerializerMethodField()
    
    class Meta:
        model = FloorAnnouncement
        fields = [
            'id', 'title', 'priority', 'status',
            'floor_wing_name', 'created_at', 'is_read'
        ]
    
    def get_floor_wing_name(self, obj):
        return obj.floor_wing.get_full_name() or obj.floor_wing.username
    
    def get_is_read(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return obj.is_read_by(request.user)
        return False
