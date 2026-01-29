from rest_framework import serializers
from .models import CLTSubmission, CLTFile
from django.contrib.auth.models import User


class CLTFileSerializer(serializers.ModelSerializer):
    """Serializer for CLT file uploads"""
    
    class Meta:
        model = CLTFile
        fields = ['id', 'file', 'file_type', 'file_name', 'file_size', 'uploaded_at']
        read_only_fields = ['id', 'uploaded_at']
    
    def create(self, validated_data):
        # Automatically set file_name and file_size if not provided
        if 'file' in validated_data and not validated_data.get('file_name'):
            validated_data['file_name'] = validated_data['file'].name
        if 'file' in validated_data and not validated_data.get('file_size'):
            validated_data['file_size'] = validated_data['file'].size
        return super().create(validated_data)


class CLTSubmissionSerializer(serializers.ModelSerializer):
    """Serializer for CLT submissions"""
    
    files = CLTFileSerializer(many=True, read_only=True)
    user_name = serializers.CharField(source='user.username', read_only=True)
    user_email = serializers.EmailField(source='user.email', read_only=True)
    reviewer_name = serializers.CharField(source='reviewed_by.username', read_only=True, allow_null=True)
    
    class Meta:
        model = CLTSubmission
        fields = [
            'id', 'user', 'user_name', 'user_email',
            'title', 'description', 'platform', 'completion_date', 'duration', 'drive_link',
            'status', 'current_step', 'files',
            'reviewer_comments', 'reviewed_by', 'reviewer_name', 'reviewed_at',
            'created_at', 'updated_at', 'submitted_at'
        ]
        read_only_fields = ['id', 'user', 'created_at', 'updated_at', 'reviewed_by', 'reviewed_at']
    
    def validate_current_step(self, value):
        """Ensure step is between 1 and 3"""
        if value < 1 or value > 3:
            raise serializers.ValidationError("Step must be between 1 and 3")
        return value
    
    def validate(self, data):
        """Additional validation"""
        # If status is being changed to submitted, require completion_date
        if data.get('status') == 'submitted' and not data.get('completion_date'):
            if not self.instance or not self.instance.completion_date:
                raise serializers.ValidationError("Completion date is required for submission")
        return data


class CLTSubmissionCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating CLT submissions with drive link"""
    
    class Meta:
        model = CLTSubmission
        fields = [
            'title', 'description', 'platform', 'completion_date', 'duration', 'drive_link',
            'current_step', 'status'
        ]
    
    def validate_duration(self, value):
        """Ensure duration is at least 10 hours"""
        if value is not None and value < 10:
            raise serializers.ValidationError("Total duration must be at least 10 hours")
        return value
    
    def create(self, validated_data):
        # Set user from context
        validated_data['user'] = self.context['request'].user
        
        # Create submission (files handled separately in view)
        submission = CLTSubmission.objects.create(**validated_data)
        
        return submission


class CLTSubmissionUpdateSerializer(serializers.ModelSerializer):
    """Serializer for updating CLT submissions"""
    
    class Meta:
        model = CLTSubmission
        fields = [
            'title', 'description', 'platform', 'completion_date', 'duration',
            'current_step', 'status'
        ]
    
    def validate_duration(self, value):
        """Ensure duration is at least 10 hours"""
        if value is not None and value < 10:
            raise serializers.ValidationError("Total duration must be at least 10 hours")
        return value
    
    def update(self, instance, validated_data):
        # If status changes to submitted, set submitted_at
        if validated_data.get('status') == 'submitted' and instance.status != 'submitted':
            from django.utils import timezone
            instance.submitted_at = timezone.now()
        
        return super().update(instance, validated_data)
