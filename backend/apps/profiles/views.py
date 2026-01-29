from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import UserProfile
from .serializers import UserProfileSerializer, UserProfileUpdateSerializer


class UserProfileView(generics.RetrieveUpdateAPIView):
    """Get and update current user's profile"""
    permission_classes = [IsAuthenticated]
    
    def get_serializer_class(self):
        if self.request.method == 'GET':
            return UserProfileSerializer
        return UserProfileUpdateSerializer
    
    def get_object(self):
        """Get or create profile for current user"""
        profile, created = UserProfile.objects.get_or_create(user=self.request.user)
        return profile
    
    def retrieve(self, request, *args, **kwargs):
        """Get user profile"""
        profile = self.get_object()
        serializer = UserProfileSerializer(profile)
        return Response(serializer.data)
    
    def update(self, request, *args, **kwargs):
        """Update user profile"""
        partial = kwargs.pop('partial', False)
        profile = self.get_object()
        serializer = self.get_serializer(profile, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        
        # Return full profile data
        response_serializer = UserProfileSerializer(profile)
        return Response(response_serializer.data)
    
    def partial_update(self, request, *args, **kwargs):
        """Partial update user profile"""
        kwargs['partial'] = True
        return self.update(request, *args, **kwargs)
