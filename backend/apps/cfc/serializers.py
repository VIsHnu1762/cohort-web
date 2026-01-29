from rest_framework import serializers
from django.contrib.auth.models import User
from .models import (
    HackathonRegistration,
    HackathonSubmission,
    BMCVideoSubmission,
    InternshipSubmission,
    GenAIProjectSubmission
)


class HackathonRegistrationSerializer(serializers.ModelSerializer):
    """Serializer for Hackathon registrations"""
    user = serializers.StringRelatedField(read_only=True)
    days_until_event = serializers.IntegerField(read_only=True)
    is_upcoming = serializers.BooleanField(read_only=True)
    
    class Meta:
        model = HackathonRegistration
        fields = [
            'id', 'user', 'hackathon_name', 'mode', 'registration_date',
            'participation_date', 'hackathon_url', 'notes', 'is_completed',
            'days_until_event', 'is_upcoming', 'submission',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'user', 'created_at', 'updated_at', 
                           'days_until_event', 'is_upcoming']


class HackathonRegistrationCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating/updating Hackathon registrations"""
    
    class Meta:
        model = HackathonRegistration
        fields = [
            'hackathon_name', 'mode', 'registration_date', 'participation_date',
            'hackathon_url', 'notes'
        ]
    
    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)


class HackathonSubmissionSerializer(serializers.ModelSerializer):
    """Serializer for Hackathon submissions"""
    user = serializers.StringRelatedField(read_only=True)
    reviewer = serializers.StringRelatedField(source='reviewed_by', read_only=True)
    
    class Meta:
        model = HackathonSubmission
        fields = [
            'id', 'user', 'hackathon_name', 'mode', 'registration_date',
            'participation_date', 'github_repo', 'certificate_link', 'status', 'current_step',
            'submitted_at', 'reviewer_comments', 'reviewer', 'reviewed_at',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'user', 'submitted_at', 'reviewer_comments', 
                           'reviewer', 'reviewed_at', 'created_at', 'updated_at']


class HackathonSubmissionCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating/updating Hackathon submissions"""
    
    class Meta:
        model = HackathonSubmission
        fields = [
            'hackathon_name', 'mode', 'registration_date', 'participation_date',
            'github_repo', 'certificate_link', 'current_step'
        ]
    
    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)


class BMCVideoSubmissionSerializer(serializers.ModelSerializer):
    """Serializer for BMC Video submissions"""
    user = serializers.StringRelatedField(read_only=True)
    reviewer = serializers.StringRelatedField(source='reviewed_by', read_only=True)
    
    class Meta:
        model = BMCVideoSubmission
        fields = [
            'id', 'user', 'video_url', 'description', 'status',
            'submitted_at', 'reviewer_comments', 'reviewer', 'reviewed_at',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'user', 'submitted_at', 'reviewer_comments',
                           'reviewer', 'reviewed_at', 'created_at', 'updated_at']


class BMCVideoSubmissionCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating/updating BMC Video submissions"""
    
    class Meta:
        model = BMCVideoSubmission
        fields = ['video_url', 'description']
    
    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)


class InternshipSubmissionSerializer(serializers.ModelSerializer):
    """Serializer for Internship submissions"""
    user = serializers.StringRelatedField(read_only=True)
    reviewer = serializers.StringRelatedField(source='reviewed_by', read_only=True)
    internship_status_display = serializers.CharField(source='get_internship_status_display', read_only=True)
    
    class Meta:
        model = InternshipSubmission
        fields = [
            'id', 'user', 'company', 'role', 'mode', 'duration',
            'internship_status', 'internship_status_display',
            'completion_certificate_link', 'lor_link', 'status',
            'submitted_at', 'reviewer_comments', 'reviewer', 'reviewed_at',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'user', 'submitted_at', 'reviewer_comments',
                           'reviewer', 'reviewed_at', 'created_at', 'updated_at',
                           'internship_status_display']


class InternshipSubmissionCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating/updating Internship submissions"""
    
    class Meta:
        model = InternshipSubmission
        fields = [
            'company', 'role', 'mode', 'duration', 'internship_status',
            'completion_certificate_link', 'lor_link'
        ]
    
    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)


class GenAIProjectSubmissionSerializer(serializers.ModelSerializer):
    """Serializer for GenAI Project submissions"""
    user = serializers.StringRelatedField(read_only=True)
    reviewer = serializers.StringRelatedField(source='reviewed_by', read_only=True)
    solution_type_display = serializers.CharField(source='get_solution_type_display', read_only=True)
    industry_display = serializers.CharField(source='get_innovation_industry_display', read_only=True)
    
    class Meta:
        model = GenAIProjectSubmission
        fields = [
            'id', 'user', 'problem_statement', 'solution_type', 'solution_type_display',
            'innovation_technology', 'innovation_industry', 'industry_display',
            'github_repo', 'demo_link', 'status', 'current_step',
            'submitted_at', 'reviewer_comments', 'reviewer', 'reviewed_at',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'user', 'submitted_at', 'reviewer_comments',
                           'reviewer', 'reviewed_at', 'created_at', 'updated_at',
                           'solution_type_display', 'industry_display']


class GenAIProjectSubmissionCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating/updating GenAI Project submissions"""
    
    class Meta:
        model = GenAIProjectSubmission
        fields = [
            'problem_statement', 'solution_type', 'innovation_technology',
            'innovation_industry', 'github_repo', 'demo_link', 'current_step'
        ]
    
    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)


class CFCStatsSerializer(serializers.Serializer):
    """Serializer for CFC statistics"""
    total_hackathons = serializers.IntegerField()
    total_bmc_videos = serializers.IntegerField()
    total_internships = serializers.IntegerField()
    total_genai_projects = serializers.IntegerField()
    approved_count = serializers.IntegerField()
    pending_count = serializers.IntegerField()
