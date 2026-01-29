from rest_framework import serializers
from .models import UserProfile
from django.contrib.auth.models import User


class UserProfileSerializer(serializers.ModelSerializer):
    """Serializer for UserProfile"""
    
    username = serializers.CharField(source='user.username', read_only=True)
    email = serializers.EmailField(source='user.email', read_only=True)
    first_name = serializers.CharField(source='user.first_name', read_only=True)
    last_name = serializers.CharField(source='user.last_name', read_only=True)
    role_display = serializers.CharField(source='get_role_display', read_only=True)
    campus_display = serializers.CharField(source='get_campus_display', read_only=True)
    floor_display = serializers.CharField(source='get_floor_display', read_only=True)
    
    class Meta:
        model = UserProfile
        fields = [
            'id', 'user', 'username', 'email', 'first_name', 'last_name',
            'role', 'role_display', 'campus', 'campus_display', 'floor', 'floor_display',
            'leetcode_id', 'github_id', 'linkedin_id',
            'assigned_mentor', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'user', 'created_at', 'updated_at']


class UserProfileUpdateSerializer(serializers.ModelSerializer):
    """Serializer for updating UserProfile"""
    
    first_name = serializers.CharField(required=False, allow_blank=True)
    last_name = serializers.CharField(required=False, allow_blank=True)
    
    class Meta:
        model = UserProfile
        fields = ['first_name', 'last_name', 'leetcode_id', 'github_id', 'linkedin_id']
    
    def validate_leetcode_id(self, value):
        """Validate LeetCode ID format"""
        if value and len(value) < 3:
            raise serializers.ValidationError("LeetCode ID must be at least 3 characters")
        return value
    
    def validate_github_id(self, value):
        """Validate GitHub ID format"""
        if value and len(value) < 3:
            raise serializers.ValidationError("GitHub ID must be at least 3 characters")
        return value
    
    def update(self, instance, validated_data):
        """Update both User and UserProfile fields"""
        # Extract User fields
        first_name = validated_data.pop('first_name', None)
        last_name = validated_data.pop('last_name', None)
        
        # Update User fields
        user = instance.user
        if first_name is not None:
            user.first_name = first_name
        if last_name is not None:
            user.last_name = last_name
        user.save()
        
        # Update UserProfile fields
        return super().update(instance, validated_data)
