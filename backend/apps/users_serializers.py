from rest_framework import serializers
from django.contrib.auth.models import User


class UserProfileSerializer(serializers.Serializer):
    """Serializer for UserProfile nested in User"""
    role = serializers.CharField()
    campus = serializers.CharField(allow_null=True)
    floor = serializers.IntegerField(allow_null=True)
    assigned_mentor = serializers.SerializerMethodField()
    
    def get_assigned_mentor(self, obj):
        if obj.assigned_mentor:
            return {
                'id': obj.assigned_mentor.id,
                'username': obj.assigned_mentor.username,
                'email': obj.assigned_mentor.email
            }
        return None


class UserSerializer(serializers.ModelSerializer):
    """Serializer for User profile"""
    profile = UserProfileSerializer(read_only=True)
    
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'is_staff', 'is_superuser', 'profile']
        read_only_fields = ['id', 'is_staff', 'is_superuser']

