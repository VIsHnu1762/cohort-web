from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import LeetCodeProfile, LeetCodeSubmission, ProgressSnapshot

User = get_user_model()


class LeetCodeSubmissionSerializer(serializers.ModelSerializer):
    """Serializer for LeetCode submissions"""
    
    class Meta:
        model = LeetCodeSubmission
        fields = [
            'id', 'problem_title', 'problem_slug', 'difficulty',
            'status', 'language', 'timestamp', 'created_at'
        ]
        read_only_fields = ['id', 'created_at']


class ProgressSnapshotSerializer(serializers.ModelSerializer):
    """Serializer for progress snapshots"""
    
    class Meta:
        model = ProgressSnapshot
        fields = [
            'id', 'total_solved', 'easy_solved', 'medium_solved',
            'hard_solved', 'ranking', 'snapshot_date'
        ]
        read_only_fields = ['id']


class LeetCodeProfileSerializer(serializers.ModelSerializer):
    """Full serializer for LeetCode profiles with nested data"""
    
    user = serializers.StringRelatedField(read_only=True)
    reviewer = serializers.StringRelatedField(read_only=True)
    submissions = LeetCodeSubmissionSerializer(many=True, read_only=True)
    snapshots = ProgressSnapshotSerializer(many=True, read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    
    class Meta:
        model = LeetCodeProfile
        fields = [
            'id', 'user', 'leetcode_username',
            'total_solved', 'easy_solved', 'medium_solved', 'hard_solved',
            'ranking', 'contest_rating', 'streak', 'monthly_problems_count', 'total_active_days',
            'submission_calendar',
            'screenshot_url', 'status', 'status_display',
            'last_synced', 'created_at', 'updated_at',
            'submitted_at', 'reviewed_at', 'reviewer', 'review_comments',
            'submissions', 'snapshots'
        ]
        read_only_fields = [
            'id', 'user', 'last_synced', 'created_at', 'updated_at',
            'submitted_at', 'reviewed_at', 'reviewer', 'status_display'
        ]


class LeetCodeProfileCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating/updating LeetCode profiles"""
    
    class Meta:
        model = LeetCodeProfile
        fields = [
            'leetcode_username', 'total_solved', 'easy_solved',
            'medium_solved', 'hard_solved', 'ranking',
            'contest_rating', 'streak', 'screenshot_url'
        ]
    
    def create(self, validated_data):
        # Inject user from context
        user = self.context['request'].user
        validated_data['user'] = user
        return super().create(validated_data)


class LeetCodeSyncSerializer(serializers.Serializer):
    """Serializer for syncing LeetCode profile data"""
    
    leetcode_username = serializers.CharField(max_length=100, required=True)
    
    def validate_leetcode_username(self, value):
        """Validate the LeetCode username format"""
        if not value or len(value.strip()) == 0:
            raise serializers.ValidationError("LeetCode username cannot be empty")
        return value.strip()
