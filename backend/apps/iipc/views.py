from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.utils import timezone
import secrets
import requests

from .models import (
    LinkedInPostVerification,
    LinkedInConnectionVerification,
    ConnectionScreenshot,
    VerifiedConnection
)
from .serializers import (
    LinkedInPostVerificationSerializer,
    LinkedInPostVerificationCreateSerializer,
    LinkedInConnectionVerificationSerializer,
    LinkedInConnectionVerificationCreateSerializer,
    IIPCStatsSerializer
)
from .linkedin_oauth import LinkedInOAuthService


class LinkedInPostVerificationViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing LinkedIn Post Verifications
    """
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return LinkedInPostVerification.objects.filter(user=self.request.user)
    
    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return LinkedInPostVerificationCreateSerializer
        return LinkedInPostVerificationSerializer
    
    def create(self, request, *args, **kwargs):
        """Override create to return full serializer with ID"""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        instance = serializer.save()
        
        # Return full serializer with ID
        output_serializer = LinkedInPostVerificationSerializer(instance)
        return Response(output_serializer.data, status=status.HTTP_201_CREATED)
    
    @action(detail=True, methods=['post'])
    def submit(self, request, pk=None):
        """Submit a post verification for review"""
        post = self.get_object()
        
        # Validate required fields
        if not post.post_url or not post.post_date:
            return Response(
                {'error': 'Please provide post URL and date before submitting.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        if not post.character_count or post.character_count <= 0:
            return Response(
                {'error': 'Please provide character count before submitting.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        post.status = 'pending'
        post.submitted_at = timezone.now()
        post.save()
        
        serializer = self.get_serializer(post)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def stats(self, request):
        """Get post verification statistics for the current user"""
        queryset = self.get_queryset()
        stats = {
            'total': queryset.count(),
            'draft': queryset.filter(status='draft').count(),
            'pending': queryset.filter(status='pending').count(),
            'approved': queryset.filter(status='approved').count(),
            'rejected': queryset.filter(status='rejected').count(),
        }
        return Response(stats)


class LinkedInConnectionVerificationViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing LinkedIn Connection Verifications
    """
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return LinkedInConnectionVerification.objects.filter(
            user=self.request.user
        ).prefetch_related('screenshots', 'verified_connections')
    
    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return LinkedInConnectionVerificationCreateSerializer
        return LinkedInConnectionVerificationSerializer
    
    def create(self, request, *args, **kwargs):
        """Override create to return full serializer with ID"""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        instance = serializer.save()
        
        # Return full serializer with ID
        output_serializer = LinkedInConnectionVerificationSerializer(instance)
        return Response(output_serializer.data, status=status.HTTP_201_CREATED)
    
    @action(detail=True, methods=['post'])
    def submit(self, request, pk=None):
        """Submit connection verification for review"""
        verification = self.get_object()
        
        # Validate required fields
        if verification.verification_method == 'screenshot':
            if not verification.screenshots.exists():
                return Response(
                    {'error': 'Please provide at least one screenshot before submitting.'},
                    status=status.HTTP_400_BAD_REQUEST
                )
        elif verification.verification_method == 'profile':
            if not verification.profile_url:
                return Response(
                    {'error': 'Please provide profile URL before submitting.'},
                    status=status.HTTP_400_BAD_REQUEST
                )
        
        # Remove total connections validation since we're not requiring it anymore
        
        verification.status = 'pending'
        verification.submitted_at = timezone.now()
        verification.save()
        
        # Return full serializer with updated status
        serializer = LinkedInConnectionVerificationSerializer(verification)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def stats(self, request):
        """Get connection verification statistics for the current user"""
        queryset = self.get_queryset()
        stats = {
            'total': queryset.count(),
            'draft': queryset.filter(status='draft').count(),
            'pending': queryset.filter(status='pending').count(),
            'approved': queryset.filter(status='approved').count(),
            'rejected': queryset.filter(status='rejected').count(),
        }
        return Response(stats)
    
    @action(detail=False, methods=['post'])
    def connect_profile(self, request):
        """
        Connect and verify LinkedIn profile
        Accepts profile_url and creates a connection verification
        """
        profile_url = request.data.get('profile_url')
        
        if not profile_url:
            return Response(
                {'error': 'profile_url is required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Validate LinkedIn URL format
        if 'linkedin.com' not in profile_url:
            return Response(
                {'error': 'Please provide a valid LinkedIn profile URL'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # In a real implementation, this would:
        # 1. Use LinkedIn OAuth to authenticate
        # 2. Fetch profile data via LinkedIn API
        # 3. Extract connection count and other details
        
        # For now, we'll simulate the connection and ask user to provide total_connections
        # We're not enforcing a minimum connections requirement anymore
        total_connections = request.data.get('total_connections', 0)
        
        # Create or update connection verification
        verification, created = LinkedInConnectionVerification.objects.get_or_create(
            user=request.user,
            verification_method='profile',
            defaults={
                'profile_url': profile_url,
                'total_connections': total_connections,
                'status': 'draft'
            }
        )
        
        if not created:
            # Update existing verification
            verification.profile_url = profile_url
            verification.total_connections = total_connections
            verification.status = 'draft'
            verification.save()
        
        serializer = LinkedInConnectionVerificationSerializer(verification)
        return Response({
            'message': 'Profile connected successfully',
            'verification': serializer.data,
            'created': created
        }, status=status.HTTP_201_CREATED if created else status.HTTP_200_OK)
    
    @action(detail=False, methods=['get'], permission_classes=[AllowAny])
    def linkedin_auth_url(self, request):
        """
        Get LinkedIn OAuth authorization URL
        Returns the URL where user should be redirected for LinkedIn login
        """
        linkedin_service = LinkedInOAuthService()
        
        # Generate random state for CSRF protection
        state = secrets.token_urlsafe(32)
        
        # Store state in session for validation (optional but recommended)
        request.session['linkedin_oauth_state'] = state
        
        auth_url = linkedin_service.get_authorization_url(state=state)
        
        return Response({
            'authorization_url': auth_url,
            'state': state
        })
    
    @action(detail=False, methods=['post'])
    def linkedin_callback(self, request):
        """
        Handle LinkedIn OAuth callback
        Exchange code for access token and fetch profile data
        """
        code = request.data.get('code')
        state = request.data.get('state')
        
        if not code:
            return Response(
                {'error': 'Authorization code is required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Validate state (CSRF protection)
        stored_state = request.session.get('linkedin_oauth_state')
        if stored_state and state != stored_state:
            return Response(
                {'error': 'Invalid state parameter. Possible CSRF attack.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        linkedin_service = LinkedInOAuthService()
        
        try:
            # Verify LinkedIn profile and get data
            profile_data = linkedin_service.verify_profile(code)
            
            # Clear the state from session
            if 'linkedin_oauth_state' in request.session:
                del request.session['linkedin_oauth_state']
            
            return Response({
                'success': True,
                'profile': profile_data,
                'message': 'LinkedIn profile verified successfully'
            })
            
        except requests.exceptions.HTTPError as e:
            return Response(
                {'error': f'LinkedIn API error: {str(e)}'},
                status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            return Response(
                {'error': f'Failed to verify LinkedIn profile: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    @action(detail=False, methods=['get'])
    def all_stats(self, request):
        """Get combined IIPC statistics"""
        posts = LinkedInPostVerification.objects.filter(user=request.user)
        connections = LinkedInConnectionVerification.objects.filter(user=request.user)
        
        stats = {
            'total_posts': posts.count(),
            'total_connections': connections.count(),
            'approved_posts': posts.filter(status='approved').count(),
            'approved_connections': connections.filter(status='approved').count(),
            'pending_posts': posts.filter(status='pending').count(),
            'pending_connections': connections.filter(status='pending').count(),
        }
        
        serializer = IIPCStatsSerializer(stats)
        return Response(serializer.data)
