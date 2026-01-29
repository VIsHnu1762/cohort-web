from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth.models import User
from django.contrib.auth import authenticate


class EmailTokenObtainPairSerializer(TokenObtainPairSerializer):
    """
    Custom JWT serializer that accepts email or username for authentication
    """
    username_field = 'username'  # This will accept the field name as 'username' but can contain email
    
    def validate(self, attrs):
        # Get the username field (which might contain email)
        username_or_email = attrs.get('username')
        password = attrs.get('password')
        
        # Try to find user by email first, then by username
        user = None
        try:
            # Check if it's an email
            if '@' in username_or_email:
                user_obj = User.objects.filter(email=username_or_email).first()
                if user_obj:
                    user = authenticate(username=user_obj.username, password=password)
            else:
                user = authenticate(username=username_or_email, password=password)
        except Exception:
            pass
        
        if user is None:
            from rest_framework_simplejwt.exceptions import AuthenticationFailed
            raise AuthenticationFailed('No active account found with the given credentials')
        
        # Generate tokens
        refresh = self.get_token(user)
        
        # Get user profile info
        profile_data = {}
        if hasattr(user, 'profile'):
            profile = user.profile
            profile_data = {
                'role': profile.role,
                'role_display': profile.get_role_display(),
                'campus': profile.campus,
                'campus_display': profile.get_campus_display() if profile.campus else None,
                'floor': profile.floor,
                'floor_display': profile.get_floor_display() if profile.floor else None,
            }
        
        data = {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            'user': {
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'profile': profile_data
            }
        }
        
        return data
